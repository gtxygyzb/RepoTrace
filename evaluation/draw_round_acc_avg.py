#!/usr/bin/env python3
"""Aggregate round-vs-accuracy (and reward) across ALL tasks: RepoTrace vs base.

Unlike draw_round_acc.py (one chart per task), this computes the AVERAGE
per-round accuracy over every task and draws a single figure with two lines
(vanilla/base vs RepoTrace). It also prints the per-round average reward.

For each task it locates the LATEST trial under
    <root>/<task>/harbor_jobs/<model>/<latest_timestamp>/<slug>/
and reads each round's test-stdout.txt (accuracy = success_count/total_cases
from the CASE_SUMMARY line) and reward.txt (binary 1/0).

A task is skipped when its RepoTrace run has no rounds or a build-error round
(no CASE_SUMMARY). Averages are per-round over the tasks that report that round.

Usage (run inside lhy_megatron_debug, which has matplotlib):
  python evaluation/draw_round_acc_avg.py \
    --repotrace results/cc__deepseek-v4-pro__repotrace \
    --vanilla   results/cc__deepseek-v4-pro__base \
    --model deepseek-v4-pro --name cc_deepseek-v4-pro --out evaluation/round_acc
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt  # noqa: E402

BLUE = "#1f77b4"
RED = "#d62728"


def find_latest_trial_slug(root: Path, task: str, model: str) -> Path | None:
    """Return the newest <timestamp>/<slug>/ dir under root/<task>/harbor_jobs/<model>/."""
    base = root / task / "harbor_jobs" / model
    ts_dirs = sorted(base.glob("*/"))  # lexicographic == chronological
    if not ts_dirs:
        return None
    slugs = sorted(ts_dirs[-1].glob("*/"))
    return slugs[-1] if slugs else None


def round_data(slug: Path) -> tuple[dict[int, float], dict[int, float], bool]:
    """Return (accuracy, reward, has_build_error) for a trial slug."""
    acc: dict[int, float] = {}
    reward: dict[int, float] = {}
    has_build_error = False
    for stdout in sorted(slug.glob("steps/round-*/verifier/test-stdout.txt")):
        m = re.search(r"round-(\d+)", str(stdout))
        if not m:
            continue
        r = int(m.group(1))
        text = stdout.read_text(errors="replace")
        sm = re.search(r"CASE_SUMMARY total_cases=(\d+) success_count=(\d+)", text)
        if sm:
            total = int(sm.group(1))
            success = int(sm.group(2))
            acc[r] = (success / total) if total else 0.0
        else:
            has_build_error = True
            acc[r] = 0.0
        reward_file = stdout.parent / "reward.txt"
        if reward_file.exists():
            try:
                reward[r] = float(reward_file.read_text().strip())
            except (ValueError, OSError):
                reward[r] = 0.0
    return acc, reward, has_build_error


def _avg(series: dict[int, list[float]]) -> dict[int, float]:
    return {r: statistics.mean(vals) for r, vals in sorted(series.items()) if vals}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repotrace", required=True)
    ap.add_argument("--vanilla", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", default="evaluation/round_acc")
    args = ap.parse_args()

    repotrace_root = Path(args.repotrace)
    vanilla_root = Path(args.vanilla)
    out = Path(args.out) / f"{args.name}_avg.png"

    tasks = sorted(d.name for d in repotrace_root.glob("theme_*") if d.is_dir())
    if not tasks:
        print("no tasks found", file=sys.stderr)
        sys.exit(1)

    r_acc_series: dict[int, list[float]] = {}
    v_acc_series: dict[int, list[float]] = {}
    r_rew_series: dict[int, list[float]] = {}
    v_rew_series: dict[int, list[float]] = {}
    n_used = 0
    skipped = 0

    for task in tasks:
        r_slug = find_latest_trial_slug(repotrace_root, task, args.model)
        if r_slug is None:
            print(f"skip {task}: no repotrace trial", file=sys.stderr)
            skipped += 1
            continue
        r_acc, r_reward, r_build_err = round_data(r_slug)
        if not r_acc:
            print(f"skip {task}: no rounds", file=sys.stderr)
            skipped += 1
            continue
        if r_build_err:
            print(f"skip {task}: build error in repotrace", file=sys.stderr)
            skipped += 1
            continue

        v_slug = find_latest_trial_slug(vanilla_root, task, args.model)
        v_acc, v_reward, _ = round_data(v_slug) if v_slug else ({}, {}, False)

        for r, a in r_acc.items():
            r_acc_series.setdefault(r, []).append(a)
        for r, a in v_acc.items():
            v_acc_series.setdefault(r, []).append(a)
        for r, w in r_reward.items():
            r_rew_series.setdefault(r, []).append(w)
        for r, w in v_reward.items():
            v_rew_series.setdefault(r, []).append(w)
        n_used += 1

    if n_used == 0:
        print("no usable tasks", file=sys.stderr)
        sys.exit(1)

    r_acc_avg = _avg(r_acc_series)
    v_acc_avg = _avg(v_acc_series)
    r_rew_avg = _avg(r_rew_series)
    v_rew_avg = _avg(v_rew_series)

    # ---- text summary -------------------------------------------------------
    print(f"tasks used: {n_used}  (skipped: {skipped})")
    print(f"{'round':>5} | {'base acc':>8} {'repo acc':>8} | {'base rew':>8} {'repo rew':>8} | n_tasks")
    rounds = sorted(set(r_acc_avg) | set(v_acc_avg))
    for r in rounds:
        n = len(r_acc_series.get(r, []))
        print(f"{r:>5} | {v_acc_avg.get(r, float('nan')):>8.3f} "
              f"{r_acc_avg.get(r, float('nan')):>8.3f} | "
              f"{v_rew_avg.get(r, float('nan')):>8.3f} "
              f"{r_rew_avg.get(r, float('nan')):>8.3f} | {n}")

    # Round-weighted mean (equal weight per round) — sensitive to the small-n
    # tail rounds, so ALSO report a task-weighted mean (equal weight per task).
    overall_v = statistics.mean(v_acc_avg.values())
    overall_r = statistics.mean(r_acc_avg.values())
    # Task-weighted: each task contributes its own mean-round accuracy.
    task_v = []
    task_r = []
    for task in tasks:
        r_slug = find_latest_trial_slug(repotrace_root, task, args.model)
        v_slug = find_latest_trial_slug(vanilla_root, task, args.model)
        ra, _, re = round_data(r_slug) if r_slug else ({}, {}, False)
        va, _, _ = round_data(v_slug) if v_slug else ({}, {}, False)
        if va:
            task_v.append(statistics.mean(va.values()))
        if ra and not re:
            task_r.append(statistics.mean(ra.values()))
    tw_v = statistics.mean(task_v) if task_v else float("nan")
    tw_r = statistics.mean(task_r) if task_r else float("nan")
    print(f"\noverall mean accuracy (round-weighted): base={overall_v:.3f}  repotrace={overall_r:.3f}  "
          f"(delta={overall_r - overall_v:+.3f})")
    print(f"overall mean accuracy (task-weighted): base={tw_v:.3f}  repotrace={tw_r:.3f}  "
          f"(delta={tw_r - tw_v:+.3f})")

    # ---- single figure: round vs average accuracy ---------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))
    xs = rounds
    ax.plot(xs, [v_acc_avg.get(r, float("nan")) for r in xs], "o-",
            label=f"base ({tw_v:.1%})", color=BLUE, linewidth=1.8, markersize=5)
    ax.plot(xs, [r_acc_avg.get(r, float("nan")) for r in xs], "s-",
            label=f"RepoTrace ({tw_r:.1%})", color=RED, linewidth=1.8, markersize=5)

    ax.set_xlabel("Round")
    ax.set_ylabel("Average accuracy (over tasks)")
    ax.set_ylim(0.0, 1.02)
    ax.set_title(f"{args.name} — round accuracy, RepoTrace vs base (avg over {n_used} tasks)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

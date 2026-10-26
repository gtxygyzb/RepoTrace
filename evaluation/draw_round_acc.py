#!/usr/bin/env python3
"""Draw round-vs-accuracy (and round-vs-reward) charts: RepoTrace vs vanilla.

For each task under --repotrace it locates the LATEST RepoTrace trial and the
corresponding vanilla trial, reads each round's test-stdout.txt (accuracy =
success_count / total_cases) and reward.txt (binary 1/0), then draws TWO charts
per task:

  <short_task>.png         round vs accuracy (y-axis auto-zooms to the data)
  <short_task>_reward.png  round vs binary reward (0/1)

A task whose RepoTrace run contains any build-error round (no CASE_SUMMARY line)
is skipped entirely.

Usage (run inside lhy_megatron_debug, which has matplotlib):
  python evaluation/draw_round_acc.py \
    --repotrace results/t2__qwen3.7-max__repotrace \
    --vanilla   data/EvoCodeBench \
    --model qwen3.7-max --name t2_qwen3.7-max --out evaluation/round_acc
"""

from __future__ import annotations

import argparse
import re
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
            # build aborted before any CASE_SUMMARY -> mark as build error
            has_build_error = True
            acc[r] = 0.0
        reward_file = stdout.parent / "reward.txt"
        if reward_file.exists():
            try:
                reward[r] = float(reward_file.read_text().strip())
            except (ValueError, OSError):
                reward[r] = 0.0
    return acc, reward, has_build_error


def short_name(task: str) -> str:
    """theme_d10_w2_ml_ai_mlops_brownfield_modification -> d10_w2."""
    m = re.search(r"(d\d+_w\d+)", task)
    return m.group(1) if m else task


def _accuracy_ylim(*series: dict[int, float]) -> tuple[float, float]:
    """Bottom-anchored auto zoom: pin top at 1.02, zoom bottom to the min value."""
    vals = [v for s in series for v in s.values()]
    if not vals:
        return (-0.05, 1.05)
    lo = max(0.0, min(vals) - 0.06)
    return (lo, 1.02)


def _plot(task: str, rounds: list[int], vanilla_vals: list[float | None],
          repotrace_vals: list[float | None], out_path: Path, *,
          reward: bool) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(rounds, vanilla_vals, "o-", label="vanilla", color=BLUE,
            linewidth=1.6, markersize=4)
    ax.plot(rounds, repotrace_vals, "s-", label="RepoTrace", color=RED,
            linewidth=1.6, markersize=4)

    ax.set_xlabel("Round")
    if reward:
        ax.set_ylabel("Reward (all cases pass)")
        ax.set_ylim(-0.1, 1.1)
        ax.set_title(f"{short_name(task)} — per-round reward")
    else:
        ax.set_ylabel("Accuracy")
        ax.set_ylim(*_accuracy_ylim(
            {r: v for r, v in zip(rounds, vanilla_vals) if v is not None},
            {r: v for r, v in zip(rounds, repotrace_vals) if v is not None},
        ))
        ax.set_title(f"{short_name(task)} — round accuracy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repotrace", required=True, help="RepoTrace results root dir")
    ap.add_argument("--vanilla", required=True, help="Vanilla baseline root dir")
    ap.add_argument("--model", required=True, help="Model bucket name, e.g. qwen3.7-max")
    ap.add_argument("--name", required=True, help="Output folder name, e.g. t2_qwen3.7-max")
    ap.add_argument("--out", default="evaluation/round_acc", help="Output root dir")
    args = ap.parse_args()

    repotrace_root = Path(args.repotrace)
    vanilla_root = Path(args.vanilla)
    out_root = Path(args.out) / args.name

    tasks = sorted(d.name for d in repotrace_root.glob("theme_*") if d.is_dir())
    if not tasks:
        print(f"no tasks found under {repotrace_root}", file=sys.stderr)
        sys.exit(1)

    for task in tasks:
        r_slug = find_latest_trial_slug(repotrace_root, task, args.model)
        if r_slug is None:
            print(f"skip {task}: no repotrace trial", file=sys.stderr)
            continue
        r_acc, r_reward, r_build_err = round_data(r_slug)
        if not r_acc:
            print(f"skip {task}: no rounds in repotrace", file=sys.stderr)
            continue
        if r_build_err:
            print(f"skip {task}: build error in repotrace run", file=sys.stderr)
            continue

        v_slug = find_latest_trial_slug(vanilla_root, task, args.model)
        v_acc, v_reward, _ = round_data(v_slug) if v_slug else ({}, {}, False)

        rounds = sorted(set(r_acc) | set(v_acc))
        base = out_root / short_name(task)

        # accuracy chart
        _plot(task, rounds,
              [v_acc.get(r) for r in rounds],
              [r_acc.get(r) for r in rounds],
              Path(f"{base}.png"), reward=False)

        # reward chart (binary)
        _plot(task, sorted(set(r_reward) | set(v_reward)),
              [v_reward.get(r) for r in sorted(set(r_reward) | set(v_reward))],
              [r_reward.get(r) for r in sorted(set(r_reward) | set(v_reward))],
              Path(f"{base}_reward.png"), reward=True)

        print(f"wrote {base}.png + {base}_reward.png  (repotrace={len(r_acc)}r, vanilla={len(v_acc)}r)")

    print(f"done: {out_root}")


if __name__ == "__main__":
    main()

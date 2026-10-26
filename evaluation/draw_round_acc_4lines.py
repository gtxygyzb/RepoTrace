#!/usr/bin/env python3
"""Round-vs-metric line chart for 4 DeepSeek-V4-Pro combos (2 harnesses x base/RepoTrace).

Lines (latest trial per task, averaged over tasks that have that round):
  Claude base / Claude RepoTrace / T2 base(vanilla) / T2 RepoTrace

Draws TWO files: round-vs-mean-reward and round-vs-mean-accuracy.

Usage (run inside lhy_megatron_debug, which has matplotlib):
  python evaluation/draw_round_acc_4lines.py --out evaluation/round_acc/cc_t2_ds_v4
"""

from __future__ import annotations

import argparse
import re
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

MAX_ROUND = 10

# (task-scan-root, model-bucket, label, color, linestyle)
# Same harness = same color; base = dashed, RepoTrace = solid.
COMBOS = [
    ("results/cc__deepseek-v4-pro__base",      "deepseek-v4-pro", "Claude base",      "#1f77b4", "--"),
    ("results/cc__deepseek-v4-pro__repotrace", "deepseek-v4-pro", "Claude RepoTrace", "#1f77b4", "-"),
    ("data/EvoCodeBench",                      "deepseek-v4-pro", "T2 base",          "#2ca02c", "--"),
    ("results/t2__deepseek-v4-pro__repotrace", "deepseek-v4-pro", "T2 RepoTrace",     "#2ca02c", "-"),
]


def latest_slug(root: Path, task: str, model: str) -> Path | None:
    base = root / task / "harbor_jobs" / model
    ts = sorted(base.glob("*/"))
    if not ts:
        return None
    slugs = sorted(ts[-1].glob("*/"))
    return slugs[-1] if slugs else None


def round_metrics(slug: Path) -> tuple[dict[int, float], dict[int, float]]:
    """Return (reward, accuracy) per round (binary reward, case-level accuracy)."""
    rew: dict[int, float] = {}
    acc: dict[int, float] = {}
    for stdout in slug.glob("steps/round-*/verifier/test-stdout.txt"):
        m = re.search(r"round-(\d+)", str(stdout))
        if not m:
            continue
        r = int(m.group(1))
        if r > MAX_ROUND:
            continue
        text = stdout.read_text(errors="replace")
        sm = re.search(r"CASE_SUMMARY total_cases=(\d+) success_count=(\d+)", text)
        if sm:
            total = int(sm.group(1)); success = int(sm.group(2))
            acc[r] = (success / total) if total else 0.0
        rf = stdout.parent / "reward.txt"
        if rf.exists():
            try:
                rew[r] = 1.0 if float(rf.read_text().strip()) >= 0.999 else 0.0
            except (ValueError, OSError):
                pass
    return rew, acc


def _mean(series: dict[int, list[float]]) -> dict[int, float]:
    return {r: statistics.mean(v) for r, v in sorted(series.items()) if v}


def _plot(metric_series: list[dict[int, float]], labels: list[str], colors: list[str],
          linestyles: list[str], ylabel: str, title: str, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    rounds = sorted({r for s in metric_series for r in s})
    for s, lab, c, ls in zip(metric_series, labels, colors, linestyles):
        ax.plot(rounds, [s.get(r, float("nan")) for r in rounds],
                marker="o", label=lab, color=c, linestyle=ls,
                linewidth=1.8, markersize=5)
    ax.set_xlabel("Round")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0.0, 1.02)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="evaluation/round_acc/cc_t2_ds_v4")
    args = ap.parse_args()

    labels = [c[2] for c in COMBOS]
    colors = [c[3] for c in COMBOS]
    linestyles = [c[4] for c in COMBOS]
    rew_series: list[dict[int, list[float]]] = [{} for _ in COMBOS]
    acc_series: list[dict[int, list[float]]] = [{} for _ in COMBOS]

    for i, (root_str, model, label, _, _) in enumerate(COMBOS):
        root = Path(root_str)
        for task in sorted(d.name for d in root.glob("theme_*") if d.is_dir()):
            slug = latest_slug(root, task, model)
            if slug is None:
                continue
            rew, acc = round_metrics(slug)
            for r, v in rew.items():
                rew_series[i].setdefault(r, []).append(v)
            for r, v in acc.items():
                acc_series[i].setdefault(r, []).append(v)
        print(f"{label:18s} reward rounds={sorted(rew_series[i])}  acc rounds={sorted(acc_series[i])}")

    rew_avg = [_mean(s) for s in rew_series]
    acc_avg = [_mean(s) for s in acc_series]

    _plot(rew_avg, labels, colors, linestyles, "Mean reward (fraction passing)",
          "DeepSeek-V4-Pro — round mean reward (latest run, avg over tasks)",
          Path(f"{args.out}_reward.png"))
    _plot(acc_avg, labels, colors, linestyles, "Mean accuracy",
          "DeepSeek-V4-Pro — round mean accuracy (latest run, avg over tasks)",
          Path(f"{args.out}_acc.png"))

    print(f"\nwrote {args.out}_reward.png and {args.out}_acc.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Heatmap: agent+model (rows) x round 1-10 (cols) = average accuracy over tasks.

For each experiment dir under results/ (name convention <scaffold>__<model>__<variant>,
e.g. cc__deepseek-v4-pro__repotrace), locate the LATEST trial per task under
    <root>/<task>/harbor_jobs/<model>/<latest_timestamp>/<slug>/
read each round's test-stdout.txt `CASE_SUMMARY total_cases=.. success_count=..`
(accuracy = success/total), and average over the tasks that HAVE that round
(tasks missing a round are simply not counted for it). Only rounds 1-10.

Usage (run inside lhy_megatron_debug, which has matplotlib):
  python evaluation/heatmap_round_acc.py --out evaluation/round_acc/heatmap_round_acc.png
"""

from __future__ import annotations

import argparse
import re
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np

MAX_ROUND = 10

# (task-scan-root, model-bucket, y-axis label) — order is the heatmap row order.
# `data/EvoCodeBench` is the official vanilla baseline (terminus-2, no injection).
COMBOS = [
    ("results/cc__deepseek-v4-pro__base",      "deepseek-v4-pro", "Claude + DS-V4-Pro  (base)"),
    ("results/cc__deepseek-v4-pro__repotrace", "deepseek-v4-pro", "Claude + DS-V4-Pro  (RepoTrace)"),
    ("data/EvoCodeBench",                      "deepseek-v4-pro", "T2 + DS-V4-Pro  (base / vanilla)"),
    ("results/t2__deepseek-v4-pro__repotrace", "deepseek-v4-pro", "T2 + DS-V4-Pro  (RepoTrace)"),
]


def latest_slug(root: Path, task: str, model: str) -> Path | None:
    """Newest <timestamp>/<slug>/ dir under root/<task>/harbor_jobs/<model>/."""
    base = root / task / "harbor_jobs" / model
    ts_dirs = sorted(base.glob("*/"))  # lexicographic == chronological
    if not ts_dirs:
        return None
    slugs = sorted(ts_dirs[-1].glob("*/"))
    return slugs[-1] if slugs else None


def round_reward(slug: Path) -> dict[int, float]:
    """Per-round binary reward: 1.0 = all cases passed, 0.0 = otherwise."""
    rew: dict[int, float] = {}
    for rf in slug.glob("steps/round-*/verifier/reward.txt"):
        m = re.search(r"round-(\d+)", str(rf))
        if not m:
            continue
        r = int(m.group(1))
        if r > MAX_ROUND:
            continue
        try:
            v = float(rf.read_text(errors="replace").strip())
            rew[r] = 1.0 if v >= 0.999 else 0.0
        except (ValueError, OSError):
            continue
    return rew


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-root", default="results")
    ap.add_argument("--out", default="evaluation/round_acc/heatmap_round_acc.png")
    args = ap.parse_args()

    results_root = Path(args.results_root)
    out = Path(args.out)

    rounds = list(range(1, MAX_ROUND + 1))
    n_combos = len(COMBOS)
    mean = np.full((n_combos, MAX_ROUND), np.nan)
    n_tasks = np.zeros((n_combos, MAX_ROUND), dtype=int)

    for i, (root_str, model, label) in enumerate(COMBOS):
        root = Path(root_str)
        if not root.is_dir():
            print(f"skip {root_str}: not found", file=__import__("sys").stderr)
            continue
        series: dict[int, list[float]] = {}
        for task in sorted(d.name for d in root.glob("theme_*") if d.is_dir()):
            slug = latest_slug(root, task, model)
            if slug is None:
                continue
            for r, a in round_reward(slug).items():
                series.setdefault(r, []).append(a)
        for r, vals in series.items():
            mean[i, r - 1] = statistics.mean(vals)
            n_tasks[i, r - 1] = len(vals)
        n_total = len(list(root.glob("theme_*")))
        print(f"{label:35s} -> rounds with data: {sorted(series)} (tasks scanned: {n_total})")

    # ---- heatmap ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 4.2))
    cmap = plt.get_cmap("RdYlGn").copy()
    cmap.set_bad("#e0e0e0")
    masked = np.ma.masked_invalid(mean)
    im = ax.imshow(masked, cmap=cmap, vmin=0.0, vmax=1.0, aspect="auto")

    ax.set_xticks(range(MAX_ROUND))
    ax.set_xticklabels([str(r) for r in rounds])
    ax.set_yticks(range(n_combos))
    ax.set_yticklabels([c[2] for c in COMBOS])
    ax.set_xlabel("Round")
    ax.set_title("Average round reward (all cases pass = 1, latest run) — first 10 rounds")

    for i in range(n_combos):
        if np.isnan(mean[i]).all():
            ax.text(MAX_ROUND / 2 - 0.5, i, "no completed rounds yet",
                    ha="center", va="center", fontsize=9, color="#666666",
                    style="italic")
            continue
        for j in range(MAX_ROUND):
            v = mean[i, j]
            if np.isnan(v):
                continue
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=9, color="black")
            if n_tasks[i, j]:
                ax.text(j, i + 0.32, f"(n={n_tasks[i, j]})", ha="center",
                        va="center", fontsize=6.5, color="#333333")

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Mean reward (fraction of tasks passing)")
    ax.set_ylim(n_combos - 0.5, -0.5)  # row 0 on top

    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

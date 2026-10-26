#!/usr/bin/env python3
"""Per-round average PASS RATE (case-level) from test-stdout.txt.

reward.txt is binary (1 only if EVERY case in the round passes), so for weak
models it collapses to ~0 and hides partial progress. This instead reads
    <results-dir>/<task>/harbor_jobs/<model>/<latest_timestamp>/<slug>/
        steps/round-N/verifier/test-stdout.txt
parses the `CASE_SUMMARY total_cases=X success_count=Y` line, and reports, for
each round, the average pass rate (success/total) over the tasks that HAVE that
round. Only the LATEST trial per task is used.

Usage:
  python evaluation/compute_round_pass_rate.py \
      --results-dir results/t2__qwen3.7-max__repotrace --model qwen3.7-max
"""

from __future__ import annotations

import argparse
import re
import statistics
from pathlib import Path

MAX_ROUND = 20


def latest_slug(root: Path, task: str, model: str) -> Path | None:
    base = root / task / "harbor_jobs" / model
    ts = sorted(base.glob("*/"))  # lexicographic == chronological
    if not ts:
        return None
    slugs = sorted(ts[-1].glob("*/"))
    return slugs[-1] if slugs else None


def round_pass_rate(slug: Path) -> dict[int, float]:
    pr: dict[int, float] = {}
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
            total = int(sm.group(1))
            success = int(sm.group(2))
            pr[r] = (success / total) if total else 0.0
    return pr


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--max-round", type=int, default=10)
    args = ap.parse_args()

    root = Path(args.results_dir)
    series: dict[int, list[float]] = {}
    n_scanned = 0
    n_used = 0
    for task in sorted(d.name for d in root.glob("theme_*") if d.is_dir()):
        n_scanned += 1
        slug = latest_slug(root, task, args.model)
        if slug is None:
            continue
        pr = round_pass_rate(slug)
        if not pr:
            continue
        n_used += 1
        for r, v in pr.items():
            series.setdefault(r, []).append(v)

    if not series:
        print("no rounds found", file=__import__("sys").stderr)
        return

    print(f"tasks scanned: {n_scanned}   tasks with data: {n_used}")
    print(f"{'round':>5} | {'avg pass rate':>14} | n_tasks")
    overall = []
    for r in sorted(series):
        vals = series[r]
        if r > args.max_round:
            continue
        avg = statistics.mean(vals)
        overall.append(avg)
        print(f"{r:>5} | {avg:>14.3f} | {len(vals)}")
    print("-" * 35)
    print(f"{'overall':>5} | {statistics.mean(overall):>14.3f} | "
          f"(mean of rounds 1-{args.max_round})")


if __name__ == "__main__":
    main()

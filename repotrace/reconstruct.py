"""Reconstruct the agent's actual workspace from harbor ATIF trajectories.

terminus-2 writes files by typing `cat > <path> << 'EOF' ... EOF` into the
session; the full heredoc content is preserved in each tool_call's
`arguments.keystrokes`. This replays those writes (and `mkdir`) into a local
tree so we can re-run the structure collector on the REAL files the agent
produced (function-level edges etc.).

Usage:
    python3 -m repotrace.reconstruct <trial-dir> --out /tmp/recon
<trial-dir> is a harbor trial dir with steps/round-N/agent/trajectory.json.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from pathlib import Path

from .graph import _SOURCE_EXT

_HEREDOC_QUOTED = re.compile(
    r"cat\s+>\s+(\S+)\s+<<\s*'([A-Za-z0-9_]+)'\s*\n(.*?)\n\2(?=\s*\n|$)",
    re.DOTALL,
)
_HEREDOC_RAW = re.compile(
    r"cat\s+>\s+(\S+)\s+<<\s*([A-Za-z0-9_]+)\s*\n(.*?)\n\2(?=\s*\n|$)",
    re.DOTALL,
)
# python inline writes:  content = '''<body>'''  with open('<path>','w') as f
_PY_WRITE = re.compile(
    r"content\s*=\s*'''(.*?)'''\s*with\s+open\(['\"]([^'\"]+)['\"],\s*['\"]w['\"]\)",
    re.DOTALL,
)
_MKDIR = re.compile(r"mkdir\s+(?:-p\s+)?([^\s\n;]+)")


def _iter_keystrokes(trial: Path):
    for tj in sorted(glob.glob(str(trial / "steps/round-*/agent/trajectory.json"))):
        try:
            data = json_load(tj)
        except Exception:  # noqa: BLE001
            continue
        for step in data.get("steps", []):
            for tc in step.get("tool_calls") or []:
                ks = (tc.get("arguments") or {}).get("keystrokes", "")
                if ks:
                    yield Path(tj).parent.name, ks


def json_load(p):
    import json
    return json.load(open(p))


def reconstruct(trial: Path, out_dir: Path) -> dict[str, str]:
    """Write files under out_dir; return {relpath: source_round}."""
    written: dict[str, str] = {}
    for round_name, ks in _iter_keystrokes(trial):
        for m in _HEREDOC_QUOTED.finditer(ks):
            target, delim, content = m.group(1), m.group(2), m.group(3)
            # drop trailing content after closing delimiter
            content = content.rstrip("\n")
            _write(out_dir, target, content)
            written.setdefault(_rel(target), round_name)
        for m in _HEREDOC_RAW.finditer(ks):
            # only if not already captured by the quoted pass for same target
            target, delim, content = m.group(1), m.group(2), m.group(3)
            if _rel(target) in written:
                continue
            content = content.rstrip("\n")
            _write(out_dir, target, content)
            written.setdefault(_rel(target), round_name)
        for m in _MKDIR.finditer(ks):
            p = Path(m.group(1))
            if p.is_absolute():
                (out_dir / p.relative_to(p.anchor)).mkdir(parents=True, exist_ok=True)
        for m in _PY_WRITE.finditer(ks):
            content, target = m.group(1), m.group(2)
            content = content.rstrip("\n")
            # careful: content may itself contain ''' (Go string literals with
            # triple single quotes are impossible; fine for our use)
            _write(out_dir, target, content)
            written.setdefault(_rel(target), round_name)
    return written


def _rel(target: str) -> str:
    t = Path(target)
    if t.is_absolute():
        # workspace root is /app; normalize /app/cmd/... -> cmd/...
        parts = t.parts
        if "app" in parts:
            parts = parts[parts.index("app") + 1:]
        return str(Path(*parts))
    return str(t)


def _write(out_dir: Path, target: str, content: str) -> None:
    rel = _rel(target)
    p = out_dir / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content + "\n")


def reconcile(trial: Path, out_dir: Path) -> dict[str, str]:
    """Normalize reconstructed paths against the final manifest (round_N_graph
    file list). Returns {final_relpath: status('ok'|'starter'|'missing')}.

    Files the agent wrote from scratch are replayed from the trajectory; files
    it only edited in place (e.g. a C project's starter sources) are filled from
    the task's own environment starter, and labeled 'starter'.
    """
    graphs = sorted(glob.glob(str(trial / "steps/round-*/agent/repotrace/round_*_graph.json")))
    if not graphs:
        return {}
    manifest = [f["path"] for f in json_load(graphs[-1]).get("files", [])]
    task_dir = _find_task_dir(trial)
    starter_root = task_dir / "environment/app" if task_dir is not None else None
    # index reconstructed files by basename (last-write wins)
    by_base: dict[str, Path] = {}
    for p in sorted(out_dir.rglob("*")):
        if p.is_file():
            by_base.setdefault(p.name, p)
    status: dict[str, str] = {}
    manifest_set = set(manifest)
    for rel in manifest:
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        src = by_base.get(rel.rsplit("/", 1)[-1])
        if src is not None:
            if src != target:
                target.write_text(src.read_text())
            status[rel] = "ok"
            continue
        # not captured from the trajectory -> fill from the task starter
        if starter_root is not None and (starter_root / rel).is_file():
            target.write_text((starter_root / rel).read_text())
            status[rel] = "starter"
        else:
            status[rel] = "missing"
    # Drop abandoned draft artifacts (non-source files not in the manifest:
    # test fixtures, tmp files, stray json, etc.). Keep every SOURCE file even
    # if the old run's manifest missed it (e.g. the pre-shell collector never
    # recorded .sh files, yet they are the agent's real work).
    for p in sorted(out_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(out_dir))
        if rel in manifest_set:
            continue
        if not rel.endswith(_SOURCE_EXT):
            p.unlink()
    return status


def _find_task_dir(trial: Path) -> Path | None:
    """Find data/EvoCodeBench/<task> that owns this trial dir (the path segment
    that exists under the data root)."""
    data_root = Path(__file__).resolve().parent.parent / "data/EvoCodeBench"
    for seg in trial.parts:
        cand = data_root / seg
        if cand.is_dir():
            return cand
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("trial", type=Path)
    ap.add_argument("--out", type=Path, default=Path("/tmp/repotrace_recon"))
    a = ap.parse_args()
    written = reconstruct(a.trial, a.out)
    print(f"reconstructed {len(written)} files -> {a.out}")
    status = reconcile(a.trial, a.out)
    if status:
        n_ok = sum(1 for v in status.values() if v == "ok")
        n_starter = sum(1 for v in status.values() if v == "starter")
        n_miss = sum(1 for v in status.values() if v == "missing")
        print(f"reconciled against final manifest: {n_ok} ok, "
              f"{n_starter} from-starter, {n_miss} missing")
        for rel, st in sorted(status.items()):
            if st == "missing":
                print(f"  MISSING {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

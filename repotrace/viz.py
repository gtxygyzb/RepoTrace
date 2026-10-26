"""Render a per-round RepoTrace report: rewards, tokens, entity extraction, and
NESTED graphs — outer layer = files (clusters), inner layer = their functions,
edges = function-level calls ACROSS files.

Usage:
    python3 -m repotrace.viz <trial-dir> [--out report.html] [--base <base-job>]
        [--recon <reconstructed-workspace>]

<trial-dir> is a harbor trial dir with steps/round-N/{verifier,agent}/.
By default each round's graph comes from the persisted repotrace artifacts.
Pass --recon <dir> (a workspace reconstructed by repotrace.reconstruct) to
re-collect each round with function-level call edges: for round N only the
files that existed at round N (from the persisted manifest) are used, so the
call graph shows how the architecture grew.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .graph import COLLECT_SCRIPT, parse_collect_output


def _read_round_graph(trial: Path, n: int) -> dict | None:
    hits = glob.glob(str(trial / f"steps/round-{n}/agent/repotrace/round_{n}_graph.json"))
    if not hits:
        return None
    return json.loads(open(hits[0]).read())


def _read_round_trace(trial: Path, n: int) -> dict | None:
    hits = glob.glob(str(trial / f"steps/round-{n}/agent/repotrace/round_{n}_trace.json"))
    if not hits:
        return None
    return json.loads(open(hits[0]).read())


def _rewards(trial: Path, n_rounds: int) -> list[int | None]:
    """Per-round pass/fail. reward.txt may hold '0', '1', '0.0' or '1.0';
    any value >= 0.5 counts as a pass."""
    out = []
    for n in range(1, n_rounds + 1):
        f = trial / f"steps/round-{n}/verifier/reward.txt"
        if not f.exists():
            out.append(None)
            continue
        try:
            val = float(f.read_text().strip() or 0)
        except ValueError:
            val = 0.0
        out.append(1 if val >= 0.5 else 0)
    return out


def _round_count(trial: Path) -> int:
    return len(list((trial / "steps").glob("round-*"))) if (trial / "steps").is_dir() else 9


def _collect_round_graph(recon: Path, trial: Path, n: int) -> dict | None:
    """Collect the graph from the full reconstructed workspace.

    The recon tree is the agent's final workspace (trajectory-replayed writes +
    starter-filled files), so we collect it whole. Subsetting to the old
    persisted manifest is deliberately NOT done: for pre-multi-language
    collector runs the manifest missed .sh files, so subsetting would throw
    away the agent's real work. Future runs persist accurate per-round graphs
    in-container and don't need --recon at all.
    """
    if not any(recon.iterdir()):
        return None
    out = subprocess.run(["sh", "-s", str(recon)], input=COLLECT_SCRIPT,
                         capture_output=True, text=True, timeout=180)
    g = parse_collect_output(out.stdout)
    return {
        "files": [
            {
                "path": f,
                "pagerank": round(g.pagerank.get(f, 0.0), 6),
                "fan_in": g.fan_in.get(f, 0),
                "fan_out": g.fan_out.get(f, 0),
            }
            for f in sorted(g.files)
        ],
        "edges": sorted([list(e) for e in g.edges]),
        "func_edges": sorted([[list(a), list(b)] for a, b in g.func_edges]),
        "func_defs": {k: sorted(v) for k, v in g.func_defs.items()},
    }


def _pr_map(graph: dict) -> dict[str, float]:
    return {f["path"]: f.get("pagerank", 0.0) for f in graph.get("files", [])
            if isinstance(f, dict)}


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", name)


def _paths(files: list) -> list[str]:
    return [f["path"] if isinstance(f, dict) else f for f in files]


def _dot_compound_svg(graph: dict, inter_only: bool = False) -> str:
    """Nested graph: file clusters -> function nodes -> function call edges.

    ALL edges are deduplicated at the data model level (func_edges is a set:
    at most one edge per caller/callee function pair). Shows every function
    edge: cross-file = solid dark, intra-file = faint dashed. Pass inter_only
    to hide the intra-file edges.
    """
    if shutil.which("dot") is None:
        return "<p>(graphviz `dot` not installed)</p>"
    files = _paths(graph.get("files", []))
    func_edges = graph.get("func_edges", []) or []
    func_defs = graph.get("func_defs", {}) or {}
    if not files:
        return "<p>(empty graph)</p>"

    file_funcs: dict[str, list[str]] = {}
    for fname, fileset in func_defs.items():
        for f in fileset:
            file_funcs.setdefault(f, []).append(fname)

    L = ["digraph rt {", "rankdir=LR;", "compound=true;",
         'node [shape=box, style="rounded,filled", fontsize=9, fillcolor="#ffffff", margin="0.06,0.03"];']
    for f in sorted(files):
        funcs = sorted(file_funcs.get(f, []))
        short = f.rsplit("/", 1)[-1]
        L.append(f'  subgraph cluster_{_safe(f)} {{')
        L.append(f'    label="{short}"; style="rounded,filled"; fillcolor="#f4f6f8"; color="#b0b8c0"; fontsize=10;')
        for fn in funcs:
            L.append(f'    "{f}:{fn}";')
        L.append("  }")
    # inter-file edges emphasized solid; intra-file edges faint dashed
    for (cf, fn), (df, cal) in func_edges:
        if cf == df:
            if not inter_only:
                L.append(f'  "{cf}:{fn}" -> "{df}:{cal}" [color="#bbbbbb", style="dashed", arrowsize=0.4];')
        else:
            L.append(f'  "{cf}:{fn}" -> "{df}:{cal}" [color="#33415c", arrowsize=0.5];')
    L.append("}")
    try:
        svg = subprocess.run(["dot", "-Tsvg"], input="\n".join(L),
                             capture_output=True, text=True, timeout=30).stdout
        return svg or "<p>dot produced no output</p>"
    except Exception as e:  # noqa: BLE001
        return f"<p>dot failed: {e}</p>"


def _dot_file_svg(graph: dict) -> str:
    """Fallback: plain file-level graph (when no function data)."""
    if shutil.which("dot") is None:
        return "<p>(graphviz `dot` not installed)</p>"
    files = graph.get("files", [])
    if not files:
        return "<p>(empty graph)</p>"
    L = ["digraph rt {", "rankdir=LR;", 'node [shape=box, style="rounded", fontsize=9];']
    for f in sorted(files, key=lambda x: x["path"]):
        L.append(f'  "{f["path"]}" [label="{f["path"].rsplit("/", 1)[-1]}"];')
    for a, b in graph.get("edges", []) or []:
        L.append(f'  "{a}" -> "{b}" [color="#33415c", arrowsize=0.5];')
    L.append("}")
    try:
        return subprocess.run(["dot", "-Tsvg"], input="\n".join(L),
                              capture_output=True, text=True, timeout=30).stdout
    except Exception as e:  # noqa: BLE001
        return f"<p>dot failed: {e}</p>"


def _fmt_files(files: list[str], n: int = 8) -> str:
    if not files:
        return "(none)"
    body = ", ".join(files[:n])
    return body + (f" … +{len(files) - n}" if len(files) > n else "")


def build_report(trial: Path, out_path: Path, base: Path | None = None,
                 recon: Path | None = None, inter_only: bool = False) -> str:
    n = _round_count(trial)
    rewards = _rewards(trial, n)

    def _job_result(p: Path):
        best = None
        for d in (p, p.parent, p.parent.parent):
            r = d / "result.json"
            if not r.exists():
                continue
            if best is None:
                best = r
            try:
                if "n_input_tokens" in json.loads(r.read_text()).get("stats", {}):
                    return r
            except (json.JSONDecodeError, ValueError):
                continue
        return best

    tokens: dict | None = None
    jr = _job_result(trial)
    if jr is not None:
        s = json.loads(jr.read_text()).get("stats", {})
        tokens = {k: s.get(k) for k in ("n_input_tokens", "n_output_tokens", "n_cache_tokens")}
    base_tokens: dict | None = None
    bjr = _job_result(base) if base is not None else None
    if bjr is not None:
        s = json.loads(bjr.read_text()).get("stats", {})
        base_tokens = {k: s.get(k) for k in ("n_input_tokens", "n_output_tokens")}

    tok_line = "<p>tokens not found</p>"
    if tokens and tokens["n_input_tokens"]:
        b_in = base_tokens.get("n_input_tokens") if base_tokens else None
        pct = f"  <b>({(tokens['n_input_tokens'] / b_in - 1) * 100:+.0f}% vs base)</b>" if b_in else ""
        tok_line = (f"<p>input <b>{tokens['n_input_tokens']:,}</b>{pct} · output "
                    f"{tokens['n_output_tokens']:,} · cache {tokens['n_cache_tokens']:,}</p>")

    reward_cells = []
    for i, r in enumerate(rewards, 1):
        color = "#4caf50" if r == 1 else "#e53935" if r == 0 else "#888"
        reward_cells.append(
            f'<div style="display:inline-block;width:34px;height:34px;line-height:34px;'
            f'text-align:center;margin:2px;color:#fff;background:{color};'
            f'border-radius:4px;font-weight:bold">{i}</div>')

    round_blocks = []
    for i in range(1, n + 1):
        t = _read_round_trace(trial, i)
        ents = (t or {}).get("entities", {})
        delta = (t or {}).get("graph", {}).get("delta", {})
        color = "#4caf50" if rewards[i - 1] == 1 else "#e53935"
        if recon is not None:
            g = _collect_round_graph(recon, trial, i)
            # recon failed to reproduce this round's files -> fall back to the
            # persisted snapshot (accurate file list, even without edges)
            if not (g or {}).get("files"):
                g = _read_round_graph(trial, i)
            has_func = bool((g or {}).get("func_edges"))
            svg = _dot_compound_svg(g, inter_only) if has_func else _dot_file_svg(g or {"files": []})
            nfiles = len((g or {}).get("files", []))
            nedges = len((g or {}).get("func_edges", []))
        else:
            g = _read_round_graph(trial, i)
            svg = _dot_compound_svg(g or {"files": []}, inter_only) if (g or {}).get("func_edges") \
                else _dot_file_svg(g or {"files": []})
            nfiles = len((g or {}).get("files", []))
            nedges = len((g or {}).get("func_edges", []))
        round_blocks.append(f"""
        <tr>
          <td style="border:1px solid #ddd;padding:8px;width:96px;vertical-align:top">
            <b>Round {i}</b><br><span style="color:{color}">{'PASS' if rewards[i-1]==1 else 'FAIL'}</span><br>
            <small>{nfiles} files · {nedges} call edges<br>src={ents.get('source','?')}</small>
          </td>
          <td style="border:1px solid #ddd;padding:8px;vertical-align:top;width:26%">
            <small><b>targets:</b> {_fmt_files(ents.get('target_files', []))}<br>
            <b>symbols:</b> {_fmt_files(ents.get('target_symbols', []), 6)}<br>
            <b>affected_prior:</b> {_fmt_files(ents.get('affected_prior', []), 6)}<br>
            <b>files_added:</b> {_fmt_files(delta.get('files_added', []))}</small>
          </td>
          <td style="border:1px solid #ddd;padding:8px;text-align:center">{svg}</td>
        </tr>""")

    base_name = f" (vs {base.name})" if base else ""
    recon_note = ("<p><b>Graphs re-collected from the reconstructed agent workspace "
                  f"({recon}) with function-level call edges.</b> Boxes = files, inner "
                  "nodes = functions, arrows = function calls (solid = cross-file, "
                  "dashed = intra-file).</p>" if recon else
                  "<p>Graphs from persisted snapshots. Pass <code>--recon</code> to "
                  "re-collect with function-level call edges.</p>")
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>RepoTrace — {trial.name}</title></head><body style="font-family:sans-serif">
<h2>RepoTrace per-round report — {trial.name}</h2>
<h3>Rewards: {sum(1 for r in rewards if r == 1)}/{len(rewards)} passed</h3>
<div>{''.join(reward_cells)}</div>
{tok_line}
{recon_note}
<table style="border-collapse:collapse;width:100%">
<thead><tr><th style="text-align:left">Round</th><th style="text-align:left">Extraction</th>
<th style="text-align:left">Architecture & call graph</th></tr></thead>
{''.join(round_blocks)}
</table>
<p><small>RepoTrace artifacts persisted at steps/round-N/agent/repotrace/.</small></p>
</body></html>"""
    out_path.write_text(html)
    return str(out_path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("trial", type=Path)
    ap.add_argument("--out", type=Path, default=Path("repotrace_report.html"))
    ap.add_argument("--base", type=Path, default=None)
    ap.add_argument("--recon", type=Path, default=None)
    ap.add_argument("--inter-only", action="store_true",
                    help="hide intra-file (dashed) edges; default shows ALL "
                         "deduplicated function edges (intra dashed + inter solid)")
    a = ap.parse_args()
    print("report:", build_report(a.trial, a.out, a.base, a.recon, a.inter_only))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Fuse the repo structure analysis and requirement entities into an
advisory repository-guidance message injected into the agent.

Design — two things the agent cannot easily get by itself (especially a
rich-tool agent like claude-code that can Read every file):
  1. Structural centrality — which files are hubs and what a change ripples
     into (graph analysis, not derivable from just reading files).
  2. Cross-round state — what is already in place from prior rounds and what
     this round adds (compensates for the stateless per-round conversation).

Deliberately NOT provided:
  * requirement localization ("this request lands in main.go") — a rich-tool
    agent can find that itself by reading; restating it is redundant noise;
  * raw import/call edge dumps — also derivable by reading;
  * a round-by-round history ("round 1 ... round 2 ...") — invites longitudinal
    planning and re-triggers over-engineering;
  * mandatory workflow / "must" / "do not" injunctions;
  * raw PageRank / fan-in numbers presented as facts without context.
"""

from __future__ import annotations

from .entities import RequirementEntities
from .graph import RepoGraph


def _short_role(f: str) -> str:
    """A short semantic role derived from the file basename."""
    name = f.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
    if name == "main":
        return "CLI entry point"
    if "pipeline" in name:
        return "pipeline logic"
    if "report" in name:
        return "report generation"
    if "run" in name:
        return "experiment execution"
    if "validate" in name:
        return "validation"
    if "plan" in name:
        return "planning"
    if "artifact" in name:
        return "artifact storage"
    if "compare" in name:
        return "comparison"
    if "sweep" in name:
        return "analysis"
    if "state" in name:
        return "state management"
    if "export" in name:
        return "export"
    return "implementation"


def _build_command(g: RepoGraph) -> str | None:
    """Infer a build/verify command from the repo's source languages."""
    exts = {f.rsplit(".", 1)[-1].lower() for f in g.files}
    if "go" in exts:
        return "go build ./..."
    if exts & {"c", "cc", "cpp", "cxx"}:
        return "make"
    if "py" in exts:
        return "python -m py_compile <changed files>"
    if exts & {"sh", "bash"}:
        return "bash -n <changed script>"
    return None


def build_message(
    graph: RepoGraph,
    ent: RequirementEntities,
    round_no: int,
    max_impact: int = 25,
    trace: list[dict] | None = None,
) -> str:
    lines: list[str] = []
    add = lines.append
    file_set = set(graph.files)

    add("=" * 72)
    add(f"[RepoTrace] Repository guidance for the current request (round {round_no})")
    add("The notes below summarize structural centrality and cross-round state.")
    add("They are supplemental context — use your own judgment to implement.")
    add("=" * 72)

    # ---- Structural centrality: hubs + impact scope ------------------------
    add("")
    add("## Structural centrality")
    hubs = sorted(
        [f for f in graph.files if graph.fan_in.get(f, 0) >= 2],
        key=lambda f: graph.fan_in.get(f, 0),
        reverse=True,
    )[:5]
    if hubs:
        for f in hubs:
            n = graph.fan_in.get(f, 0)
            deps = graph.dependents([f], hops=1, cap=4)
            s = f"  - {f} is depended on by {n} files"
            if deps:
                s += f" (e.g. {', '.join(deps)})"
            add(s + "; changing it ripples widely.")
    else:
        add("  (no file is depended on by multiple others)")

    # ---- Cross-round state: existing components + this round's delta --------
    add("")
    add("## Cross-round state")
    existing = sorted(graph.files, key=lambda f: graph.fan_in.get(f, 0), reverse=True)
    add("Already present (from prior rounds):")
    for f in existing[:8]:
        add(f"  - {f}: {_short_role(f)}")
    absent = [f for f in ent.target_files if f not in file_set]
    if absent:
        add("New in this round (to be created):")
        for f in absent:
            add(f"  - {f}")
    if ent.affected_prior:
        add("Prior components this round may touch:")
        for p in ent.affected_prior[:6]:
            add(f"  - {p}")

    # ---- Verification -------------------------------------------------------
    cmd = _build_command(graph)
    add("")
    add("## Verification")
    if cmd:
        add(f"  - Build and run tests after modification, e.g. `{cmd}`.")
    else:
        add("  - Build and run tests after modification.")

    # ---- Practical note (terminal constraint) -------------------------------
    add("")
    add("## Practical note")
    add("  The terminal can hang on very large heredocs. Write files in several "
        "smaller pieces.")

    add("=" * 72)
    return "\n".join(lines)

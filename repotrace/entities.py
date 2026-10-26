"""Requirement entity extraction: LLM-based, with a deterministic fallback.

Extracts target files / symbols / behavior constraints from a natural-language
round instruction, grounded in the actual repository inventory.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from .graph import RepoGraph


@dataclass
class RequirementEntities:
    target_files: list[str] = field(default_factory=list)
    target_symbols: list[str] = field(default_factory=list)
    behavior_constraints: list[str] = field(default_factory=list)
    affected_prior: list[str] = field(default_factory=list)
    summary: str = ""
    source: str = "none"  # "llm" | "fallback"


_PROMPT = """You are analyzing one round of a multi-round software evolution task.

Below is the current repository structure (ranked by structural importance),
the accumulated requirement-code trace from previous rounds, and the NEW user
requirement for this round.

## Repository files (top {n_top} by structural weight, of {n_files} total)
{top_files}

## Full file inventory (truncated)
{all_files}

## Key symbols (name -> files, truncated)
{symbols}
{prev_block}
## New requirement for this round (round {round_no})
{instruction}

Extract the requirement entities FOR THIS ROUND. Use the previous-round trace
to tell apart what is ALREADY implemented (prior rounds' targets — usually do
NOT re-list them unless the new requirement modifies them) from what this
round newly demands. Return ONLY a JSON object (no prose):
{{
  "target_files": ["repo-relative paths the requirement directly asks to create/modify"],
  "target_symbols": ["functions/classes/types the requirement names or clearly implies"],
  "behavior_constraints": ["observable behaviors that must hold after this round"],
  "affected_prior": ["prior-round components whose behavior this round may break or change"],
  "summary": "one sentence: what this round demands"
}}
Only list files/symbols plausibly present (or to be created) in THIS repo."""

_PREV_TEMPLATE = """
## Requirement-code trace from previous rounds (already implemented)
{rounds}

## Structural changes since last round
{delta}
"""


def _parse_json_loose(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        return d if isinstance(d, dict) else None
    except (json.JSONDecodeError, ValueError):
        return None


def _format_prev_rounds(trace: list[dict], max_rounds: int = 6) -> str:
    """Compact rendering of the accumulated requirement-code trace."""
    lines = []
    for rec in trace[-max_rounds:]:
        e = rec.get("entities", {})
        lines.append(
            f"  round {rec.get('round')}: {e.get('summary', '')[:200]} "
            f"| targets={e.get('target_files', [])[:5]} "
            f"| syms={e.get('target_symbols', [])[:5]}"
        )
    return "\n".join(lines)


def _format_delta(delta: dict | None, max_items: int = 15) -> str:
    if not delta:
        return "(no previous round — this is the first round)"
    parts = []
    if delta.get("files_added"):
        parts.append("files_added: " + ", ".join(delta["files_added"][:max_items]))
    if delta.get("files_removed"):
        parts.append("files_removed: " + ", ".join(delta["files_removed"][:max_items]))
    if delta.get("edges_added"):
        parts.append("edges_added: " + str(len(delta["edges_added"])))
    if delta.get("edges_removed"):
        parts.append("edges_removed: " + str(len(delta["edges_removed"])))
    return "\n".join(parts) or "(no structural change detected)"


async def extract_entities_llm(
    instruction: str,
    graph: RepoGraph,
    model: str,
    api_base: str | None = None,
    *,
    round_no: int = 0,
    trace: list[dict] | None = None,
    delta: dict | None = None,
) -> RequirementEntities | None:
    """LLM extraction via litellm (host side). Returns None on any failure.

    trace/delta carry the accumulated previous-round state so the extraction is
    grounded in what is ALREADY implemented (cross-round tracking), not a fresh
    per-round analysis.
    """
    import litellm  # harbor dependency, always available in the agent process

    top = graph.top(30)
    sym_items = list(graph.symbol_files.items())[:150]
    if trace:
        prev_block = _PREV_TEMPLATE.format(
            rounds=_format_prev_rounds(trace),
            delta=_format_delta(delta),
        )
    else:
        prev_block = (
            "\n## Requirement-code trace from previous rounds\n"
            "(none — this is round 1; treat the requirement as starting fresh)\n"
        )
    prompt = _PROMPT.format(
        n_top=len(top),
        n_files=len(graph.files),
        top_files="\n".join(top),
        all_files="\n".join(graph.files[:400]),
        symbols="\n".join(f"{k}: {sorted(v)[:4]}" for k, v in sym_items),
        prev_block=prev_block,
        round_no=round_no,
        instruction=instruction[:8000],
    )
    kwargs: dict = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        # It emits a long hidden
        # `reasoning_content` (chain-of-thought) BEFORE the real `content`.
        # The reasoning can stretch into the tens of thousands of tokens, so a
        # small cap (the original 4000) lets reasoning consume the whole budget
        # and returns empty `content` -> silent fallback. Cap high enough to
        # never truncate; the model still stops on its own once the JSON is out.
        "max_tokens": 65536,
    }
    if api_base:
        kwargs["api_base"] = api_base
    resp = await litellm.acompletion(**kwargs)
    msg = resp.choices[0].message
    content = msg.content or ""
    d = _parse_json_loose(content)
    if not d:
        # The reasoning phase sometimes already contains the JSON draft; if the
        # final answer came back empty, mine it from there as a last resort.
        rc = getattr(msg, "reasoning_content", None) or ""
        d = _parse_json_loose(rc)
    if not d:
        return None
    return RequirementEntities(
        target_files=[str(x) for x in d.get("target_files", [])][:20],
        target_symbols=[str(x) for x in d.get("target_symbols", [])][:20],
        behavior_constraints=[str(x) for x in d.get("behavior_constraints", [])][:10],
        affected_prior=[str(x) for x in d.get("affected_prior", [])][:15],
        summary=str(d.get("summary", "")),
        source="llm",
    )


def extract_entities_fallback(
    instruction: str,
    graph: RepoGraph,
    *,
    round_no: int = 0,
    trace: list[dict] | None = None,
    delta: dict | None = None,
) -> RequirementEntities:
    """Deterministic keyword matching — no LLM needed, never fails.

    Cross-round awareness: if the new instruction references a symbol or file
    from a PREVIOUS round's targets, it lands in affected_prior instead of
    target_* (i.e. it's an existing component this round may touch, not a new
    one to create).
    """
    prior_files: set[str] = set()
    prior_syms: set[str] = set()
    if trace:
        for rec in trace:
            prior_files.update(rec.get("entities", {}).get("target_files", []))
            prior_syms.update(rec.get("entities", {}).get("target_symbols", []))
    ent = RequirementEntities(source="fallback")
    # file paths mentioned verbatim (incl. `backticked`)
    for m in re.finditer(r"[A-Za-z0-9_./-]+\.(?:go|py|js|jsx|ts|tsx|java|rs|rb|c|h|cc|cpp|json|toml|yaml|yml|md)", instruction):
        p = m.group(0).lstrip("/")
        for f in graph.files:
            if f == p or f.endswith("/" + p):
                ent.target_files.append(f)
                break
    # identifiers: backticked or CamelCase / snake_case tokens that match symbols
    idents = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_]*)`", instruction))
    idents |= set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{3,}\b", instruction))
    for tok in sorted(idents):
        locs = graph.symbol_files.get(tok)
        # skip ubiquitous symbols (defined in many files) — too generic to
        # localize a requirement
        if locs and len(locs) <= 5:
            (ent.affected_prior if tok in prior_syms else ent.target_symbols).append(tok)
    # files referenced in the instruction that were previous-round targets
    # are "affected prior components", not new targets
    ent.affected_prior = sorted(set(ent.affected_prior + [
        f for f in ent.target_files if f in prior_files]))[:15]
    ent.target_files = sorted(f for f in ent.target_files if f not in prior_files)[:20]
    ent.target_symbols = sorted(set(ent.target_symbols))[:20]
    ent.summary = instruction.strip().splitlines()[0][:200] if instruction.strip() else ""
    return ent

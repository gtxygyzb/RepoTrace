"""RepoTraceCore: per-trial orchestration and cross-round trace persistence.

One instance lives inside the agent for the whole trial (harbor multi-step
reuses the same agent object across rounds), so the requirement trace
accumulates naturally round by round. All artifacts go under
<logs_dir>/repotrace/ — verifier inputs and scoring are never touched.

Failure contract: ANY internal failure degrades to an empty message, i.e. the
agent behaves exactly like the vanilla baseline. The plugin can never break a
run.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from . import entities as ent_mod
from . import graph as graph_mod
from .message import build_message


class RepoTraceCore:
    def __init__(
        self,
        logs_dir: Path | str,
        model: str | None = None,
        api_base: str | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.logs_dir = Path(logs_dir)
        # entity-extraction model: explicit env wins; otherwise reuse the
        # agent's own model id when it looks litellm-compatible
        self.model = model or os.environ.get("REPOTRACE_MODEL")
        self.api_base = api_base or os.environ.get("REPOTRACE_API_BASE") or \
            os.environ.get("OPENAI_API_BASE")
        self.logger = logger or logging.getLogger("repotrace")
        self.round_no = 0
        self.trace: list[dict] = []  # the cross-round requirement trace
        self._prev_graph: graph_mod.RepoGraph | None = None
        self._script_uploaded = False
        self._script_tmp: Path | None = None

    @property
    def disabled(self) -> bool:
        return os.environ.get("REPOTRACE_OFF", "").strip() == "1"

    async def _exec(self, environment, command: str, timeout: int = 120) -> str:
        res = await environment.exec(command, timeout_sec=timeout)
        out = res.stdout or ""
        if res.return_code != 0 and res.stderr:
            out += "\n" + res.stderr
        return out

    async def _ensure_script(self, environment) -> None:
        """Upload the collect script once per trial — no shell quoting issues."""
        if self._script_uploaded:
            return
        if self._script_tmp is None:
            import tempfile
            fd, p = tempfile.mkstemp(prefix="repotrace_collect_", suffix=".sh")
            with os.fdopen(fd, "w") as f:
                f.write(graph_mod.COLLECT_SCRIPT)
            self._script_tmp = Path(p)
        await environment.upload_file(self._script_tmp, graph_mod._REMOTE_SCRIPT_PATH)
        self._script_uploaded = True

    async def _collect_graph(self, environment) -> graph_mod.RepoGraph:
        await self._ensure_script(environment)
        out = await self._exec(
            environment, f"sh {graph_mod._REMOTE_SCRIPT_PATH}", timeout=180)
        return graph_mod.parse_collect_output(out)

    async def _extract(
        self,
        instruction: str,
        graph: graph_mod.RepoGraph,
        *,
        round_no: int,
        delta: dict | None,
    ):
        kw = dict(round_no=round_no, trace=self.trace, delta=delta)
        if self.model:
            try:
                ent = await ent_mod.extract_entities_llm(
                    instruction, graph, self.model, self.api_base, **kw)
                if ent is not None:
                    return ent
                self.logger.warning("repotrace: LLM extraction unparsable, fallback")
            except Exception as e:  # noqa: BLE001 - degrade by design
                self.logger.warning("repotrace: LLM extraction failed (%s), fallback", e)
        return ent_mod.extract_entities_fallback(instruction, graph, **kw)

    def _persist(self, record: dict, message: str, graph: graph_mod.RepoGraph) -> None:
        d = self.logs_dir / "repotrace"
        d.mkdir(parents=True, exist_ok=True)
        n = record["round"]
        (d / f"round_{n}_message.md").write_text(message)
        (d / f"round_{n}_trace.json").write_text(json.dumps(record, indent=1))
        (d / f"round_{n}_graph.json").write_text(
            json.dumps(graph_mod.graph_to_dict(graph), indent=1))
        (d / "trace.json").write_text(json.dumps(self.trace, indent=1))

    async def message_for(self, instruction: str, environment) -> str:
        """Build the correspondence message for this round. '' == no injection."""
        if self.disabled:
            return ""
        try:
            self.round_no += 1
            graph = await self._collect_graph(environment)
            if not graph.files:
                self.logger.warning("repotrace: no source files under %s", graph.root)
            delta = graph_mod.graph_delta(self._prev_graph, graph)
            ent = await self._extract(
                instruction, graph, round_no=self.round_no, delta=delta)
            message = build_message(
                graph, ent, self.round_no, trace=self.trace or None)
            self.logger.info(
                "repotrace: round %s message ready (%d chars) -> %s",
                self.round_no, len(message),
                self.logs_dir / "repotrace" / f"round_{self.round_no}_message.md")
            record = {
                "round": self.round_no,
                "root": graph.root,
                "graph": {
                    "n_files": len(graph.files),
                    "n_edges": len(graph.edges),
                    "delta": delta,
                    "top10": [
                        {"file": f,
                         "pagerank": round(graph.pagerank.get(f, 0.0), 6),
                         "fan_in": graph.fan_in.get(f, 0),
                         "fan_out": graph.fan_out.get(f, 0)}
                        for f in graph.top(10)
                    ],
                },
                "entities": {
                    "source": ent.source,
                    "target_files": ent.target_files,
                    "target_symbols": ent.target_symbols,
                    "behavior_constraints": ent.behavior_constraints,
                    "affected_prior": ent.affected_prior,
                    "summary": ent.summary,
                },
                "instruction_head": instruction[:500],
            }
            self.trace.append(record)
            self._prev_graph = graph
            try:
                self._persist(record, message, graph)
            except Exception as e:  # noqa: BLE001
                self.logger.warning("repotrace: persist failed (%s)", e)
            return message
        except Exception as e:  # noqa: BLE001 - degrade by design
            self.logger.warning("repotrace: disabled for this round (%s)", e)
            return ""

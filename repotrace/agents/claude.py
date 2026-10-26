"""RepoTrace adapter for harbor's claude-code agent.

Usage (harbor CLI):
    harbor run ... --agent repotrace.agents.claude:RepoTraceClaudeCode \
        --model deepseek-v4-pro

Note: the analysis runs via environment.exec inside the task container before
the claude CLI starts each round, so it works with the same persistent
container/session semantics as the vanilla agent.
"""

from __future__ import annotations

from harbor.agents.installed.claude_code import ClaudeCode

from ..core import RepoTraceCore


class RepoTraceClaudeCode(ClaudeCode):
    """claude-code + per-round requirement-code correspondence injection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repotrace: RepoTraceCore | None = None

    def _rt(self) -> RepoTraceCore:
        if self._repotrace is None:
            self._repotrace = RepoTraceCore(logs_dir=self.logs_dir)
        return self._repotrace

    async def run(self, instruction, environment, context):
        msg = await self._rt().message_for(instruction, environment)
        if msg:
            instruction = instruction.rstrip() + "\n\n" + msg
        await super().run(instruction, environment, context)

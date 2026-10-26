"""RepoTrace adapter for harbor's terminus-2 agent.

Usage (harbor CLI):
    harbor run ... --agent repotrace.agents.terminus:RepoTraceTerminus2 \
        --model openai/deepseek-v4-pro
"""

from __future__ import annotations

from harbor.agents.terminus_2 import Terminus2

from ..core import RepoTraceCore


class RepoTraceTerminus2(Terminus2):
    """terminus-2 + per-round requirement-code correspondence injection."""

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

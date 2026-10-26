"""RepoTrace: requirement-driven repository-understanding harness plugin.

Injects a requirement-code correspondence message into the agent before each
round of an EvoCodeBench multi-step trial. Pure plugin: no harbor source or
task data is modified. Activate by pointing harbor's --agent at one of the
subclasses in repotrace.agents (e.g. repotrace.agents.terminus:RepoTraceTerminus2).

Kill switch: REPOTRACE_OFF=1 disables injection entirely (agent runs vanilla).
"""

__version__ = "0.1.0"

#!/usr/bin/env bash
# ==============================================================================
# EvoCodeBench experiment runner — runs all 26 tasks into results/<exp_name>/
#
# Usage:
#   bash scripts/run_exp.sh <exp_name>
#
# Naming convention for <exp_name>:  <scaffold>__<model>__<variant>
#   scaffold:  cc (claude-code) | t2 (terminus-2)
#   model:     deepseek-v4-pro | ...
#   variant:   base | repotrace | repotrace-nocg | ...
#   Example:   cc__deepseek-v4-pro__base
#
# Required env (agent-specific):
#   AGENT_TYPE      claude-code | terminus-2 | repotrace.claude_agent:RepoTraceClaudeCode | ...
#   AGENT_MODEL     e.g. deepseek-v4-pro  (used as the harbor_jobs/<model> bucket)
#   claude-code:    ANTHROPIC_API_KEY + ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL
#                   + HARBOR_CLAUDE_LOCAL_BIN
#   terminus-2:     OPENAI_API_KEY + OPENAI_API_BASE
#
# Results land in:
#   results/<exp_name>/<task>/harbor_jobs/<AGENT_MODEL>/<timestamp>/...
# Per-task stdout/stderr logs:
#   results/<exp_name>/_logs/<task>.log
# ==============================================================================
set -uo pipefail

EXP="${1:?usage: bash scripts/run_exp.sh <exp_name>  (e.g. cc__deepseek-v4-pro__base)}"
AGENT_TYPE="${AGENT_TYPE:?set AGENT_TYPE}"
AGENT_MODEL="${AGENT_MODEL:?set AGENT_MODEL}"

ROOT="/server/anonymous/EvoCodeBench"
RESULTS_ROOT="$ROOT/results"
LOG_DIR="$RESULTS_ROOT/$EXP/_logs"
mkdir -p "$LOG_DIR"

cd "$ROOT"
rc=0
for task in data/EvoCodeBench/theme_*; do
    [ -d "$task" ] || continue
    [ -f "$task/task.toml" ] || continue
    name=$(basename "$task")
    echo "===== $name ====="
    bash evaluation/run_single.sh "$task" agent \
        --jobs-dir "$RESULTS_ROOT/$EXP/$name/harbor_jobs/${AGENT_MODEL##*/}" \
        2>&1 | tee "$LOG_DIR/$name.log"
    [ "${PIPESTATUS[0]}" -eq 0 ] || { echo "WARN: $name exited non-zero (see $LOG_DIR/$name.log)"; rc=1; }
done
echo "===== experiment $EXP done (rc=$rc) ====="
exit "$rc"

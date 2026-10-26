#!/usr/bin/env bash
# ==============================================================================
# RepoTrace — run the REMAINING tasks on claude-code + deepseek-v4-pro.
#
# Complements evaluation/run_5_repotrace_cc-deepseekv4-pro.sh: that script
# already ran 5 tasks (d10_w2 / d10_w4 / d10_w9 / d10_w11 / d1_w5), so this one
# runs every OTHER task (the remaining 21). Results land in the SAME bucket:
#   results/cc__deepseek-v4-pro__repotrace/<task>/harbor_jobs/deepseek-v4-pro/
#
# A/B counterpart to results/cc__deepseek-v4-pro__base (vanilla). Everything is
# identical except AGENT_TYPE (the RepoTrace adapter injects the message).
# ==============================================================================
cd /server/anonymous/EvoCodeBench

# patched harbor (host network + docker-build 502 retry)
export HARBOR_BIN="uv --directory /server/anonymous/EvoCodeBench/harbor-local run harbor"
# make the repotrace package importable by harbor's --agent module:Class loader
export PYTHONPATH="/server/anonymous/EvoCodeBench:${PYTHONPATH:-}"

# ---- claude-code agent -> deepseek-v4-pro (anthropic-compatible endpoint) ----
export ANTHROPIC_API_KEY="REDACTED_API_KEY"
export ANTHROPIC_AUTH_TOKEN="REDACTED_API_KEY"
export ANTHROPIC_BASE_URL="https://api.example.invalid/v1"
export HARBOR_CLAUDE_LOCAL_BIN="/server/anonymous/EvoCodeBench/tools/claude-bin/claude"

# ---- RepoTrace entity extraction (host-side litellm -> deepseek openai) ------
export OPENAI_API_KEY="REDACTED_API_KEY"
export OPENAI_API_BASE="https://api.example.invalid/v1"
export REPOTRACE_MODEL="openai/deepseek-v4-pro"

# ---- agent: RepoTrace adapter around claude-code -----------------------------
export AGENT_TYPE="repotrace.agents.claude:RepoTraceClaudeCode"
export AGENT_MODEL="deepseek-v4-pro"

# already run by run_5_repotrace_cc-deepseekv4-pro.sh — skip these
SKIP=(
  theme_d10_w2_ml_ai_mlops_brownfield_modification
  theme_d10_w4_ml_ai_mlops_migration_upgrade
  theme_d10_w9_ml_ai_mlops_reproducibility_verification
  theme_d10_w11_ml_ai_mlops_automation_scripting
  theme_d1_w5_code_build_integration_e2e_wiring
)

# 绝对路径: 避免 harbor 的 CWD(=harbor-local) 把相对 --jobs-dir 解析错位置
RESULTS_ROOT="/server/anonymous/EvoCodeBench/results/cc__deepseek-v4-pro__repotrace"

for task in data/EvoCodeBench/theme_*; do
    [ -d "$task" ] || continue
    [ -f "$task/task.toml" ] || continue
    name=$(basename "$task")

    skip=0
    for s in "${SKIP[@]}"; do
        [ "$name" = "$s" ] && skip=1 && break
    done
    [ "$skip" = "1" ] && { echo "===== skip $name (already run) ====="; continue; }

    echo "===== $name ====="
    bash evaluation/run_single.sh "$task" agent \
        --jobs-dir "$RESULTS_ROOT/$name/harbor_jobs/deepseek-v4-pro"
done

echo "===== scoring ====="
bash scripts/score_exp.sh cc__deepseek-v4-pro__repotrace deepseek-v4-pro

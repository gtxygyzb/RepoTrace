cd /server/anonymous/EvoCodeBench

export ANTHROPIC_API_KEY="REDACTED_API_KEY"
export ANTHROPIC_AUTH_TOKEN="REDACTED_API_KEY"
export ANTHROPIC_BASE_URL="https://api.example.invalid/v1"
export AGENT_TYPE="claude-code"
export AGENT_MODEL="deepseek-v4-pro"
export HARBOR_CLAUDE_LOCAL_BIN="/server/anonymous/EvoCodeBench/tools/claude-bin/claude"

bash scripts/run_exp.sh cc__deepseek-v4-pro__base
bash scripts/score_exp.sh cc__deepseek-v4-pro__base deepseek-v4-pro
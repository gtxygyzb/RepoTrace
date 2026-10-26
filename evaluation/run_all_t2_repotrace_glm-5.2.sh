#!/usr/bin/env bash
# ==============================================================================
# RepoTrace — run the REMAINING tasks on terminus-2 + GLM-5.2 (Zhipu / BigModel).
#
# Iterates over every task under data/EvoCodeBench and skips any task whose
# results directory already exists under RESULTS_ROOT (i.e. already run). Safe
# to re-run: it only picks up tasks that have not been run yet.
#
# Results: results/t2__glm-5.2__repotrace/<task>/harbor_jobs/glm-5.2/
# ==============================================================================
cd /server/anonymous/EvoCodeBench

# patched harbor (host network + docker-build 502 retry)
export HARBOR_BIN="uv --directory /server/anonymous/EvoCodeBench/harbor-local run harbor"
# make the repotrace package importable by harbor's --agent module:Class loader
export PYTHONPATH="/server/anonymous/EvoCodeBench:${PYTHONPATH:-}"

# corporate proxy (7890 reaches apt/Go; the daemon default 8888 blocks Go domains)
export http_proxy=http://proxy.example.invalid:7890
export https_proxy=http://proxy.example.invalid:7890
export HTTP_PROXY=http://proxy.example.invalid:7890
export HTTPS_PROXY=http://proxy.example.invalid:7890

# terminus-2 LLM endpoint (litellm, host side) — GLM-5.2 (Zhipu BigModel, OpenAI-compatible)
export OPENAI_API_KEY="REDACTED_API_KEY"
# 注意: 这里是 base URL,不带 /chat/completions(litellm 的 openai provider 会自己拼)
export OPENAI_API_BASE="https://api.example.invalid/v1"

# agent: RepoTrace adapter around terminus-2
export AGENT_TYPE="repotrace.agents.terminus:RepoTraceTerminus2"
export AGENT_MODEL="openai/glm-5.2"
export AGENT_KWARGS='{"llm_call_kwargs":{"extra_body":{"enable_thinking":true},"max_tokens":65536},"override_setup_timeout_sec":900}'

# RepoTrace entity-extraction model (host-side litellm call)
export REPOTRACE_MODEL="openai/glm-5.2"

# 绝对路径: 避免 harbor 的 CWD(=harbor-local) 把相对 --jobs-dir 解析错位置
RESULTS_ROOT="/server/anonymous/EvoCodeBench/results/t2__glm-5.2__repotrace"

# 遍历全部任务,跳过 RESULTS_ROOT 下已经存在结果目录(=已跑过)的任务
for task in data/EvoCodeBench/theme_*; do
    [ -d "$task" ] || continue
    [ -f "$task/task.toml" ] || continue
    name=$(basename "$task")

    if [ -d "$RESULTS_ROOT/$name" ]; then
        echo "===== skip $name (already run) ====="
        continue
    fi

    echo "===== $name ====="
    bash evaluation/run_single.sh "$task" agent \
        --jobs-dir "$RESULTS_ROOT/$name/harbor_jobs/glm-5.2"
done

echo "===== scoring ====="
bash scripts/score_exp.sh t2__glm-5.2__repotrace glm-5.2

#!/usr/bin/env bash
# ==============================================================================
# Full 26-task run — terminus-2 (T2 baseline, NO RepoTrace) × qwen3.7-max.
#
# This is the fair A/B counterpart to run_all_t2_repotrace-qwen3.7-max.sh:
# EVERYTHING is identical (endpoint, model, enable_thinking, proxy, harbor)
# EXCEPT AGENT_TYPE — terminus-2 here vs the RepoTrace adapter there. So the
# only variable is the RepoTrace injection.
#
# Results: results/t2__qwen3.7-max__base/<task>/harbor_jobs/qwen3.7-max/
# ==============================================================================
cd /server/anonymous/EvoCodeBench

# patched harbor (host network + docker-build 502 retry)
export HARBOR_BIN="uv --directory /server/anonymous/EvoCodeBench/harbor-local run harbor"

# corporate proxy (7890 reaches apt/Go; the daemon default 8888 blocks Go domains)
export http_proxy=http://proxy.example.invalid:7890
export https_proxy=http://proxy.example.invalid:7890
export HTTP_PROXY=http://proxy.example.invalid:7890
export HTTPS_PROXY=http://proxy.example.invalid:7890

# terminus-2 LLM endpoint (litellm, host side) — qwen3.7-max (Alibaba DashScope)
export OPENAI_API_KEY="REDACTED_API_KEY"
export OPENAI_API_BASE="https://api.example.invalid/v1"

# plain terminus-2 (the vanilla baseline — no RepoTrace injection)
export AGENT_TYPE="terminus-2"
export AGENT_MODEL="openai/qwen3.7-max"
export AGENT_KWARGS='{"llm_call_kwargs":{"extra_body":{"enable_thinking":true}},"override_setup_timeout_sec":900}'

bash scripts/run_exp.sh t2__qwen3.7-max__base
bash scripts/score_exp.sh t2__qwen3.7-max__base qwen3.7-max

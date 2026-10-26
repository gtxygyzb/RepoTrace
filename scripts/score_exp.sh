#!/usr/bin/env bash
# ==============================================================================
# Score an experiment via the lhy_megatron_debug container (host has no py3.11
# tomllib in some envs; the container does, and /server is mounted there).
#
# Usage:
#   bash scripts/score_exp.sh <exp_name> <model> [--json]
#
# Example:
#   bash scripts/score_exp.sh cc__deepseek-v4-pro__base deepseek-v4-pro
#
# Note: no -it flags (script-friendly); run from the host.
# ==============================================================================
set -euo pipefail

EXP="${1:?usage: bash scripts/score_exp.sh <exp_name> <model> [--json]}"
MODEL="${2:?usage: bash scripts/score_exp.sh <exp_name> <model> [--json]}"
EXTRA="${3:-}"

docker exec lhy_megatron_debug bash -c "\
cd /server/anonymous/EvoCodeBench && \
python evaluation/compute_metrics.py \
  --tasks-dir data/EvoCodeBench \
  --results-dir results/$EXP \
  --model $MODEL $EXTRA"

# /train/llamacpp_finetune.sh
# 配置先: gemma3-llamacpp/train/llamacpp_finetune.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FT_BIN="${ROOT}/llama.cpp/bin/finetune"
BASE="${ROOT}/models/gemma-3-4b-it.Q4_K_M.gguf"
TRAIN="${ROOT}/data/sft/train.jsonl"
VALID="${ROOT}/data/sft/valid.jsonl"
OUT_LORA="${ROOT}/adapters/gemma3_4b_it_chat-lora.gguf"

# llama.cpp のバージョンによりオプション名は変動する点に注意
"${FT_BIN}" \
  --model "${BASE}" \
  --train-data "${TRAIN}" \
  --valid-data "${VALID}" \
  --data-format alpaca \
  --lora-out "${OUT_LORA}" \
  --lora-r 16 --lora-alpha 16 --lora-dropout 0.05 \
  --epochs 3 --batch 64 --threads 8 --lr 1e-4 --seq-len 4096

# /scripts/to_gguf_lora.sh
# 配置先: gemma3-llamacpp/scripts/to_gguf_lora.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
IN_DIR="${ROOT_DIR}/adapters/gemma3_4b_it_chat-lora"
OUT_GGUF="${ROOT_DIR}/adapters/gemma3_4b_it_chat-lora.gguf"

# ここで convert_lora_to_gguf.py or GGUF-my-LoRA を使用
# 例:
# python path/to/convert_lora_to_gguf.py \
#   --base "${ROOT_DIR}/models/gemma-3-4b-it.Q4_K_M.gguf" \
#   --adapter "${IN_DIR}/adapter_model.safetensors" \
#   --out "${OUT_GGUF}"

echo "Converted to: ${OUT_GGUF}"

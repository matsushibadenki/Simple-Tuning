# /serve/start_server.sh
# 配置先: gemma3-llamacpp/serve/start_server.sh
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LLAMA_BIN="${ROOT_DIR}/llama.cpp/bin/server"   # llama.cppを別途clone & build想定
MODEL="${ROOT_DIR}/models/gemma-3-4b-it.Q4_K_M.gguf"

# 重要: Gemma用のchatテンプレートを自動検出。必要なら --chat-template gemma を明示。
exec "${LLAMA_BIN}" \
  -m "${MODEL}" \
  --host 127.0.0.1 --port 8080 \
  -c 8192 --repeat-penalty 1.1 --temp 0.7 --verbose

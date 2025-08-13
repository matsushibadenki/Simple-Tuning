# Dockerfile
# 配置先: Simple-Tuning/Dockerfile

# -----------------------------------------------------------------------------
# Stage 1: Builder - 依存関係のインストールとllama.cppのビルド
# -----------------------------------------------------------------------------
FROM python:3.10-slim-bookworm as builder

# システムパッケージの更新とビルドツールのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 必要なPythonパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# llama.cppをcloneしてビルド
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    make server -j

# アプリケーションコードのコピー
COPY . .

# -----------------------------------------------------------------------------
# Stage 2: Runtime - 実行環境の構築
# -----------------------------------------------------------------------------
FROM python:3.10-slim-bookworm

# システムパッケージの更新と実行に必要なライブラリのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Builderステージから必要なファイルのみコピー
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app/llama.cpp/server /usr/local/bin/server
COPY --from=builder /app/src ./src
COPY --from=builder /app/main.py .
COPY --from=builder /app/models ./models
COPY --from=builder /app/adapters ./adapters
COPY --from=builder /app/data ./data

# ポートの開放
EXPOSE 8080

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
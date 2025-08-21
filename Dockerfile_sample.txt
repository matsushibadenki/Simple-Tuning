# /app/Dockerfile

# --------------------------------------------------
# 1. ビルドステージ (builder)
# --------------------------------------------------
FROM python:3.10-slim AS builder

# ビルドに必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# llama.cppをクローンしてビルド
# Linux環境なのでCPUバックエンドのみ使用
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    mkdir build && \
    cd build && \
    cmake .. \
        -DLLAMA_CURL=OFF \
        -DGGML_OPENMP=ON \
        -DGGML_NATIVE=ON \
        -DCMAKE_BUILD_TYPE=Release && \
    cmake --build . --config Release --parallel $(nproc)

# --------------------------------------------------
# 2. 最終ステージ (final)
# --------------------------------------------------
FROM python:3.10-slim

ENV APP_HOME=/app
WORKDIR $APP_HOME

# 実行に必要なパッケージのみをインストール
RUN apt-get update && apt-get install -y \
    libopenblas0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ビルドステージからコンパイル済みの実行ファイルをコピー
COPY --from=builder /llama.cpp/build/bin/llama-server /app/llama.cpp/bin/server

# アプリケーションのコードをコピー
COPY . .

# FastAPIサーバーの起動コマンド
CMD ["uvicorn", "src.simple_tuning.chat.server:app", "--host", "0.0.0.0", "--port", "8000"]
# /app/Dockerfile

# ベースイメージの指定
FROM python:3.10-slim

# 環境変数の設定
ENV APP_HOME /app
WORKDIR $APP_HOME

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# llama.cppのインストール
# llama.cppのクローン、ビルド、実行可能ファイルの移動を単一のRUN命令にまとめる
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    mkdir build && \
    cd build && \
    cmake .. -DLLAMA_CURL=OFF && \
    cmake --build . --config Release && \
    mkdir -p /app/llama.cpp/bin && \
    mv ./bin/llama-server /app/llama.cpp/bin/server

# アプリケーションのコードをコピー
COPY . .

# FastAPIサーバーの起動コマンド
CMD ["uvicorn", "src.simple_tuning.chat.server:app", "--host", "0.0.0.0", "--port", "8000"]
# Dockerfile
# 配置先: Simple-Tuning/Dockerfile
# 最も確実な公式Ubuntuイメージをベースに、必要なものを全てインストールする

FROM ubuntu:22.04

# noninteractive frontend to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# システムパッケージの更新とPython、ビルドツールのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-venv \
    git \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# python3 -> pythonエイリアスの作成
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

# 必要なPythonパッケージのインストール
COPY requirements.txt .
# numpy<2.0 を指定してインストール
RUN pip install --no-cache-dir "numpy<2.0"
RUN pip install --no-cache-dir -r requirements.txt

# llama.cppのクローン、ビルド、実行可能ファイルの移動を単一のRUN命令にまとめる
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . --config Release && \
    mkdir -p /app/llama.cpp/bin && \
    mv ./bin/server /app/llama.cpp/bin/server

# アプリケーションのソースコードなどをコピー
COPY src ./src
COPY main.py .
COPY models ./models
COPY adapters ./adapters
COPY data ./data

# ポートの開放
EXPOSE 8080

# コンテナ起動時のデフォルトコマンド
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
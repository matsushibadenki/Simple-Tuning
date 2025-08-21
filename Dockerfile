# Dockerfile
# 配置先: Simple-Tuning/Dockerfile
# 安定したPyTorch公式イメージをベースにする

FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# システムパッケージの更新とビルドツールのインストール
# gitとcmakeはllama.cppのビルドに必要
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 必要なPythonパッケージのインストール
# まずrequirements.txtをコピーして実行
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# llama.cppをcloneしてビルド
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . --config Release

# アプリケーションのソースコードなどをコピー
COPY src ./src
COPY main.py .
COPY models ./models
COPY adapters ./adapters
COPY data ./data

# ポートの開放
EXPOSE 8080

# コンテナ起動時のデフォルトコマンド
# /usr/local/bin/server へのパスを修正
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
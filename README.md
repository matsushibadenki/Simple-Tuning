# **Simple Fine-tuning Gemma Chat System (Simple-Tuning)**

## **概要**

このプロジェクトは、GoogleのGemmaモデルをベースに、llama.cppを利用した軽量なチャットシステムの運用と、LoRA/QLoRAによるファインチューニングを手軽に行うための統合環境です。

### **✨ 特徴**

* **CLIによる簡単操作**: train, start-server, chat-clientなどのコマンドで直感的に操作可能。  
* **Docker対応**: Dockerfileにより、環境構築の手間を大幅に削減し、再現性の高い実行環境を提供。  
* **自動データ整形**: JSON形式の対話データから、SFT（Supervised Fine-Tuning）用の学習データを自動で生成。  
* **効率的なファインチューニング**: LoRA/QLoRA（Unslothを利用）による効率的なモデルの微調整。  
* **GGUF連携**: 学習済みのLoRAアダプタをGGUF形式に変換し、llama.cppサーバーで直接利用可能。

## **🚀 クイックスタート (Docker)**

Dockerがインストールされていれば、以下のコマンドで環境構築からサーバー起動までを実行できます。

1. **Dockerイメージのビルド**  
   docker build \-t simple-tuning .

2. **チャットサーバーの起動**  
   docker run \-p 8080:8080 \--rm \-it simple-tuning start-server

   サーバーは http://127.0.0.1:8080 で待機します。  
3. チャットクライアントの利用  
   別のターミナルから、以下のコマンドでクライアントを起動して対話できます。  
   docker run \--network host \--rm \-it simple-tuning chat-client

## **🛠️ ローカル環境でのセットアップ**

### **1\. 依存関係のインストール**

pip install \-r requirements.txt

### **2\. モデルの準備**

llama.cppで利用するGGUF形式のモデルをmodels/ディレクトリに配置してください。

例: models/gemma-3-4b-it.Q4\_K\_M.gguf

### **3\. llama.cppのビルド (ローカル実行時のみ)**

llama.cppを別途クローンし、ビルドしておく必要があります。

git clone https://github.com/ggerganov/llama.cpp.git  
cd llama.cpp  
make server  
\# プロジェクトルートに戻る  
cd .. 

*Dockerを使用する場合、この手順は不要です。*

## **📚 プロジェクトの利用方法**

### **1\. データ準備**

data/raw/に、以下のような形式のJSONファイルを配置します。

\[  
  {  
    "system": "あなたは有能なアシスタントです。",  
    "dialogue": \[  
      {"role":"user", "content":"Aとは何？"},  
      {"role":"assistant", "content":"Aは..."}  
    \]  
  }  
\]

その後、以下のスクリプトを実行して、学習用・検証用のデータセットを生成します。

python scripts/make\_sft\_from\_json.py  
python scripts/split\_train\_valid.py

### **2\. ファインチューニングの実行**

以下のコマンドで、LoRA/QLoRAによるファインチューニングを開始します。

python main.py train

学習が完了すると、LoRAアダプタがadapters/gemma3\_4b\_it\_chat-lora/ディレクトリに保存されます。

### **3\. LoRAアダプタのGGUF変換**

学習済みLoRAをllama.cppで利用するために、GGUF形式に変換します。

bash scripts/to\_gguf\_lora.sh

*注意: to\_gguf\_lora.sh内の変換スクリプトへのパスは、ご自身の環境に合わせて修正してください。*

### **4\. チャットサーバーの起動**

llama.cppベースのAPIサーバーを起動します。

python main.py start-server

APIエンドポイント: http://127.0.0.1:8080/v1/chat/completions

### **5\. チャットクライアントの利用**

サーバーに接続し、対話を行うためのクライアントを起動します。

python main.py chat-client

## **📂 ディレクトリ構成**

Simple-Tuning/  
├── adapters/                \# 学習済みLoRAアダプタ  
├── data/  
│   ├── raw/                 \# 元の対話データ (JSON)  
│   └── sft/                 \# SFT用に整形されたデータ (JSONL)  
├── models/                  \# GGUFモデル  
├── scripts/                 \# データ整形・変換スクリプト  
├── src/  
│   └── simple\_tuning/       \# アプリケーションのソースコード  
│       ├── chat/            \# チャットクライアント/サーバー関連  
│       ├── training/        \# ファインチューニング関連  
│       ├── config.py        \# 設定ファイル  
│       └── containers.py    \# DIコンテナ  
├── main.py                  \# CLIエントリポイント  
├── Dockerfile               \# Docker環境定義  
├── requirements.txt         \# Python依存関係  
└── README.md                \# このファイル

## **💡 注意点**

* **LoRAの適用**: llama.cppサーバーでLoRAを適用するには、起動オプションに--lora adapters/your-lora.ggufを追加してください。（src/simple\_tuning/chat/server.pyを修正）  
* **チャットテンプレート**: llama.cppはモデル名からチャットテンプレートを自動検出しますが、必要であれば--chat-template gemmaのように明示的に指定してください。  
* **llama.cppのバージョン**: llama.cppのバージョンによって、コマンドラインオプションが変更される可能性があります。公式のドキュメントも合わせてご確認ください。

## **🔗 参考リンク**

* [llama.cpp 公式リポジトリ](https://github.com/ggerganov/llama.cpp)  
* [Unsloth 公式リポジトリ](https://github.com/unslothai/unsloth)  
* [Hugging Face \- Google Gemma](https://huggingface.co/google)
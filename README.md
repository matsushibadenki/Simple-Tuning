# Simple Fine-tuning Gemma Chat System（Simple-Tuning）

## 概要

このプロジェクトは、Google Gemma-3-4B-ITモデルをベースに、`llama.cpp`での軽量なチャットシステム運用と、LoRA/QLoRAによる微調整を行うための環境です。

特徴:

* **llama.cpp**をベースにした高速チャットAPIサーバ
* **JSONベースの対話データ**から学習用データを自動生成
* **LoRA/QLoRA**による軽量ファインチューニング
* 学習済LoRAを**GGUF形式**に変換し`--lora`オプションで即適用可能

---

## ディレクトリ構成

```
Simple-Tuning/
├─ models/                  # GGUFモデル/トークナイザー
├─ adapters/                # 学習で出たLoRA(GGUF)
├─ data/
│   ├─ raw/                 # 元データ(JSON)
│   ├─ sft/                 # SFT用に整形後(JSONL)
│   └─ eval/                # 評価用データ
├─ scripts/
│   ├─ make_sft_from_json.py
│   ├─ split_train_valid.py
│   └─ to_gguf_lora.sh
├─ train/
│   ├─ unsloth_train.py     # 推奨: Transformers/Unsloth学習
│   └─ llamacpp_finetune.sh # 任意: llama.cpp直接学習
├─ serve/
│   ├─ start_server.sh
│   └─ chat_client.py
└─ README.md
```

---

## セットアップ

### 1. モデル準備

Gemma-3-4B-ITのGGUFモデルを`models/`に配置します。

```bash
models/gemma-3-4b-it.Q4_K_M.gguf
```

Hugging Face等から取得し、必要に応じて`convert_hf_to_gguf.py`で変換してください。

### 2. llama.cppのビルド

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make -j
```

---

## データ準備

### 1. JSONからSFTデータ生成

`data/raw/` に以下のようなJSONを配置します:

```json
[
  {
    "system": "あなたは有能なアシスタントです。",
    "dialogue": [
      {"role":"user", "content":"Aとは何？"},
      {"role":"assistant", "content":"Aは..."}
    ]
  }
]
```

整形実行:

```bash
python scripts/make_sft_from_json.py
python scripts/split_train_valid.py
```

---

## 学習

### 推奨ルート: Transformers/Unsloth

```bash
pip install transformers datasets peft trl unsloth
python train/unsloth_train.py
```

生成されたLoRAは `adapters/` に保存されます。

### GGUF変換

```bash
bash scripts/to_gguf_lora.sh
```

---

## サーバ起動

```bash
bash serve/start_server.sh
```

APIエンドポイント: `http://127.0.0.1:8080/v1/chat/completions`

---

## チャットクライアント使用例

```bash
python serve/chat_client.py
```

---

## llama.cpp直Finetune（任意）

```bash
bash train/llamacpp_finetune.sh
```

---

## 注意点

* LoRAは**GGUF形式**に変換してから`--lora`で適用
* JSONデータはGemmaのチャットテンプレに近づけると効果的
* llama.cppのバージョンによってオプション仕様が異なるためREADME確認必須

---

## 参考

* [llama.cpp公式](https://github.com/ggerganov/llama.cpp)
* [Unsloth](https://github.com/unslothai/unsloth)
* [Hugging Face Gemma](https://huggingface.co/google)

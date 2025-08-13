# /scripts/make_sft_from_json.py
# 配置先: gemma3-llamacpp/scripts/make_sft_from_json.py
#!/usr/bin/env python3
"""
/scripts/make_sft_from_json.py

raw/*.json から Alpaca風JSONL(SFT)を生成します。
入力例(1ファイル中の配列):
[
  {
    "system": "あなたは有能なアシスタントです。",
    "dialogue": [
      {"role":"user", "content":"Aとは何？"},
      {"role":"assistant", "content":"Aは..."},
      {"role":"user", "content":"もう少し詳しく"},
      {"role":"assistant", "content":"詳細は..."}
    ],
    "tags": ["domain:a", "tone:polite"]
  },
  ...
]
"""
import json, glob, os, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "sft"
OUT.mkdir(parents=True, exist_ok=True)

def to_alpaca_items(rec):
    system = rec.get("system") or ""
    dlg = rec.get("dialogue") or []
    items = []
    ctx = system.strip()
    user_buf = None
    for turn in dlg:
        if turn["role"] == "user":
            user_buf = turn["content"].strip()
        elif turn["role"] == "assistant" and user_buf is not None:
            items.append({
                "instruction": (ctx if ctx else "Follow the instruction and answer appropriately."),
                "input": user_buf,
                "output": turn["content"].strip()
            })
            user_buf = None
    return items

def main():
    out_path = OUT / "train_all.jsonl"
    with out_path.open("w", encoding="utf-8") as wf:
        for fn in glob.glob(str(RAW / "*.json")):
            data = json.load(open(fn, "r", encoding="utf-8"))
            for rec in data:
                for item in to_alpaca_items(rec):
                    wf.write(json.dumps(item, ensure_ascii=False)+"\n")
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()

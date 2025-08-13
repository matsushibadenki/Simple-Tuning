# /scripts/split_train_valid.py
# 配置先: gemma3-llamacpp/scripts/split_train_valid.py
#!/usr/bin/env python3
"""
/scripts/split_train_valid.py
"""
import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "data" / "sft" / "train_all.jsonl"
TRN = ROOT / "data" / "sft" / "train.jsonl"
VAL = ROOT / "data" / "sft" / "valid.jsonl"

random.seed(42)
lines = [l for l in INP.read_text(encoding="utf-8").splitlines() if l.strip()]
random.shuffle(lines)
k = max(1, int(len(lines)*0.02))  # 2%を検証へ
VAL.write_text("\n".join(lines[:k])+"\n", encoding="utf-8")
TRN.write_text("\n".join(lines[k:])+"\n", encoding="utf-8")
print(f"train: {TRN}  valid: {VAL}, ratio≈{(len(lines)-k)}/{k}")

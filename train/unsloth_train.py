# /train/unsloth_train.py
# 配置先: gemma3-llamacpp/train/unsloth_train.py
#!/usr/bin/env python3
"""
/train/unsloth_train.py

- HF上の "google/gemma-3-4b-it" をベースにLoRA/QLoRA学習
- 出力: ./adapters/gemma3_4b_it_chat-lora/adapter_model.safetensors
  （※ 単GPU 12–24GB目安。CPUでもQLoRAは遅いが理論上可）
"""
from datasets import load_dataset # type: ignore
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM # type: ignore
from peft import LoraConfig, get_peft_model # type: ignore
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Iterator

ROOT: Path = Path(__file__).resolve().parents[1]
TRAIN: Path = ROOT / "data" / "sft" / "train.jsonl"
VALID: Path = ROOT / "data" / "sft" / "valid.jsonl"
OUT_DIR: Path = ROOT / "adapters" / "gemma3_4b_it_chat-lora"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID: str = "google/gemma-3-4b-it"  # 必要に応じてgemma-3-4b-itを指定
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype="auto")

lora = LoraConfig(
    r=16, lora_alpha=16, lora_dropout=0.05,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]
)
model = get_peft_model(model, lora)

def ds_from_jsonl(path: Path) -> Any:
    """Alpaca形式のJSONLからDatasetを生成"""
    def gen() -> Iterator[Dict[str, str]]:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                r: Dict[str, Any] = json.loads(line)
                prompt: str = f"[INST] {r['instruction']}\n{r['input']} [/INST]\n"
                yield {"text": prompt + r["output"]}
    
    # 元のJSONLの列情報を取得
    with open(path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        if not first_line:
            # 空のファイルの場合は空のデータセットを返す
            return load_dataset("json", data_files={"train": []}, split="train").map(lambda _: _, batched=False)
        
        column_names: List[str] = list(json.loads(first_line).keys())

    # 'text'列以外を削除
    columns_to_remove = [c for c in column_names if c != "text"]

    return load_dataset("json", data_files=str(path), split="train").map(
        lambda _: _, batched=False
    ).remove_columns(columns_to_remove)


train_ds = ds_from_jsonl(TRAIN)
valid_ds = ds_from_jsonl(VALID)

collator = DataCollatorForCompletionOnlyLM(tokenizer=tokenizer, response_template=None)

args = TrainingArguments(
    output_dir=str(OUT_DIR),
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    learning_rate=1e-4,
    logging_steps=50,
    save_steps=500,
    eval_strategy="steps",
    eval_steps=500,
    bf16=False, 
    fp16=True
)

trainer = SFTTrainer(
    model=model, 
    tokenizer=tokenizer,
    train_dataset=train_ds, 
    eval_dataset=valid_ds,
    data_collator=collator, 
    args=args,
    max_seq_length=4096
)
trainer.train()
trainer.save_model(str(OUT_DIR))
print(f"Saved LoRA to: {OUT_DIR}")
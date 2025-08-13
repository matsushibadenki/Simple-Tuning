# /train/unsloth_train.py
# 配置先: gemma3-llamacpp/train/unsloth_train.py
#!/usr/bin/env python3
"""
/train/unsloth_train.py

- HF上の "google/gemma-3-4b-it" をベースにLoRA/QLoRA学習
- 出力: ./adapters/gemma3_4b_it_chat-lora/adapter_model.safetensors
  （※ 単GPU 12–24GB目安。CPUでもQLoRAは遅いが理論上可）
"""
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from peft import LoraConfig, get_peft_model
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "data" / "sft" / "train.jsonl"
VALID = ROOT / "data" / "sft" / "valid.jsonl"
OUT_DIR = ROOT / "adapters" / "gemma3_4b_it_chat-lora"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID = "google/gemma-3-4b-it"  # 必要に応じてgemma-3-4b-itを指定
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype="auto")

lora = LoraConfig(
    r=16, lora_alpha=16, lora_dropout=0.05,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]
)
model = get_peft_model(model, lora)

def ds_from_jsonl(path):
    # Alpaca形式: instruction+input → output
    def gen():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                prompt = f"[INST] {r['instruction']}\n{r['input']} [/INST]\n"
                yield {"text": prompt + r["output"]}
    return load_dataset("json", data_files=str(path), split="train").map(
        lambda _: _, batched=False
    ).remove_columns([c for c in load_dataset("json", data_files=str(path), split="train").column_names if c!="text"])

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
    evaluation_strategy="steps",
    eval_steps=500,
    bf16=False, fp16=True
)

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer,
    train_dataset=train_ds, eval_dataset=valid_ds,
    data_collator=collator, args=args,
    max_seq_length=4096
)
trainer.train()
trainer.save_model(str(OUT_DIR))
print("Saved LoRA to:", OUT_DIR)

# src/simple_tuning/training/trainer.py
# ファインチューニング実行ロジック

import json
from pathlib import Path
from typing import Dict, Any, Iterator

from datasets import load_dataset
from trl import SFTTrainer

from ..containers import TrainingContainer

def SFTDataset(path: Path) -> Any:
    """Alpaca形式のJSONLからDatasetを生成"""
    def gen() -> Iterator[Dict[str, str]]:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                r: Dict[str, Any] = json.loads(line)
                prompt: str = f"[INST] {r['instruction']}\n{r['input']} [/INST]\n"
                yield {"text": prompt + r["output"]}
    
    return load_dataset("json", data_files=str(path), split="train")

def run_training() -> None:
    """DIコンテナを使ってSFTを実行"""
    container = TrainingContainer()
    trainer: SFTTrainer = container.trainer()
    
    print("Starting fine-tuning...")
    trainer.train()
    
    output_dir = container.config.training_args.output_dir()
    trainer.save_model(output_dir)
    print(f"Saved LoRA to: {output_dir}")
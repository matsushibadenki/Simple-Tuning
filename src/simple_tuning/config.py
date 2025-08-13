# src/simple_tuning/config.py
# 設定ファイルを管理
from pathlib import Path
from typing import List

class PathConfig:
    ROOT: Path = Path(__file__).resolve().parents[2]
    DATA: Path = ROOT / "data"
    RAW_DATA: Path = DATA / "raw"
    SFT_DATA: Path = DATA / "sft"
    EVAL_DATA: Path = DATA / "eval"
    MODELS: Path = ROOT / "models"
    ADAPTERS: Path = ROOT / "adapters"
    TRAIN_JSONL: Path = SFT_DATA / "train.jsonl"
    VALID_JSONL: Path = SFT_DATA / "valid.jsonl"
    GGUF_MODEL: Path = MODELS / "gemma-3-4b-it.Q4_K_M.gguf"
    LORA_OUT_GGUF: Path = ADAPTERS / "gemma3_4b_it_chat-lora.gguf"

class ModelConfig:
    MODEL_ID: str = "google/gemma-3-4b-it"
    TOKENIZER_NAME: str = MODEL_ID
    LORA_R: int = 16
    LORA_ALPHA: int = 16
    LORA_DROPOUT: float = 0.05
    TARGET_MODULES: List[str] = [
        "q_proj", "k_proj", "v_proj", "o_proj", 
        "gate_proj", "up_proj", "down_proj"
    ]
    MAX_SEQ_LENGTH: int = 4096

class TrainingConfig:
    OUTPUT_DIR: str = str(PathConfig.ADAPTERS / "gemma3_4b_it_chat-lora")
    PER_DEVICE_TRAIN_BATCH_SIZE: int = 2
    GRADIENT_ACCUMULATION_STEPS: int = 8
    NUM_TRAIN_EPOCHS: int = 3
    LEARNING_RATE: float = 1e-4
    LOGGING_STEPS: int = 50
    SAVE_STEPS: int = 500
    EVAL_STRATEGY: str = "steps"
    EVAL_STEPS: int = 500
    BF16: bool = False
    FP16: bool = True

class ChatConfig:
    SERVER_URL: str = "http://127.0.0.1:8080/v1/chat/completions"
    MODEL_NAME: str = "gemma3-local"
    DEFAULT_SYSTEM_PROMPT: str = "You are a helpful assistant. Answer briefly."
    DEFAULT_USER_PROMPT: str = "こんにちは、要約をお願いします。"
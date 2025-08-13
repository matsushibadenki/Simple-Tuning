# src/simple_tuning/containers.py
# DIコンテナを定義
from dependency_injector import containers, providers
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

from .config import ModelConfig, TrainingConfig, PathConfig
from .training.trainer import SFTDataset

class TrainingContainer(containers.DeclarativeContainer):
    """訓練関連の依存関係を管理するコンテナ"""

    config = providers.Configuration()

    tokenizer = providers.Factory(
        AutoTokenizer.from_pretrained,
        pretrained_model_name_or_path=ModelConfig.TOKENIZER_NAME,
        use_fast=True
    )

    base_model = providers.Factory(
        AutoModelForCausalLM.from_pretrained,
        pretrained_model_name_or_path=ModelConfig.MODEL_ID,
        torch_dtype="auto"
    )

    lora_config = providers.Singleton(
        LoraConfig,
        r=ModelConfig.LORA_R,
        lora_alpha=ModelConfig.LORA_ALPHA,
        lora_dropout=ModelConfig.LORA_DROPOUT,
        target_modules=ModelConfig.TARGET_MODULES
    )

    peft_model = providers.Factory(
        get_peft_model,
        model=base_model,
        peft_config=lora_config
    )
    
    train_dataset = providers.Factory(
        SFTDataset,
        path=PathConfig.TRAIN_JSONL
    )

    valid_dataset = providers.Factory(
        SFTDataset,
        path=PathConfig.VALID_JSONL
    )

    training_args = providers.Factory(
        TrainingArguments,
        output_dir=TrainingConfig.OUTPUT_DIR,
        per_device_train_batch_size=TrainingConfig.PER_DEVICE_TRAIN_BATCH_SIZE,
        gradient_accumulation_steps=TrainingConfig.GRADIENT_ACCUMULATION_STEPS,
        num_train_epochs=TrainingConfig.NUM_TRAIN_EPOCHS,
        learning_rate=TrainingConfig.LEARNING_RATE,
        logging_steps=TrainingConfig.LOGGING_STEPS,
        save_steps=TrainingConfig.SAVE_STEPS,
        eval_strategy=TrainingConfig.EVAL_STRATEGY,
        eval_steps=TrainingConfig.EVAL_STEPS,
        bf16=TrainingConfig.BF16,
        fp16=TrainingConfig.FP16
    )

    data_collator = providers.Factory(
        DataCollatorForCompletionOnlyLM,
        tokenizer=tokenizer,
        response_template=None
    )

    trainer = providers.Factory(
        SFTTrainer,
        model=peft_model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=data_collator,
        args=training_args,
        max_seq_length=ModelConfig.MAX_SEQ_LENGTH
    )
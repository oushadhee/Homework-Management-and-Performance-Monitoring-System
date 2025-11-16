"""
Training script for fine-tuning LLaMA 3.2 for question generation
Uses LoRA (Low-Rank Adaptation) for efficient fine-tuning
"""

import os
import torch
import argparse
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import json
from loguru import logger


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Fine-tune LLaMA 3.2 for question generation")
    
    parser.add_argument("--model_name", type=str, default="meta-llama/Llama-3.2-3B",
                       help="Base model name from HuggingFace")
    parser.add_argument("--train_file", type=str, required=True,
                       help="Path to training data file")
    parser.add_argument("--val_file", type=str, default=None,
                       help="Path to validation data file")
    parser.add_argument("--output_dir", type=str, default="./data/models/question_generator",
                       help="Output directory for model checkpoints")
    
    # Training parameters
    parser.add_argument("--num_epochs", type=int, default=3,
                       help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4,
                       help="Training batch size per device")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=4,
                       help="Gradient accumulation steps")
    parser.add_argument("--learning_rate", type=float, default=2e-4,
                       help="Learning rate")
    parser.add_argument("--max_seq_length", type=int, default=2048,
                       help="Maximum sequence length")
    
    # LoRA parameters
    parser.add_argument("--lora_r", type=int, default=16,
                       help="LoRA rank")
    parser.add_argument("--lora_alpha", type=int, default=32,
                       help="LoRA alpha")
    parser.add_argument("--lora_dropout", type=float, default=0.05,
                       help="LoRA dropout")
    
    # Optimization
    parser.add_argument("--use_4bit", action="store_true", default=True,
                       help="Use 4-bit quantization")
    parser.add_argument("--use_gradient_checkpointing", action="store_true", default=True,
                       help="Use gradient checkpointing")
    
    return parser.parse_args()


def load_and_prepare_data(train_file: str, val_file: str = None, tokenizer=None, max_length: int = 2048):
    """Load and prepare datasets"""
    
    def format_instruction(example):
        """Format data as instruction-following"""
        text = f"""### Instruction:
{example['instruction']}

### Input:
{example.get('input', '')}

### Response:
{example['output']}"""
        
        return {"text": text}
    
    # Load datasets
    data_files = {"train": train_file}
    if val_file:
        data_files["validation"] = val_file
    
    # Determine file type
    file_ext = Path(train_file).suffix
    if file_ext == ".jsonl":
        dataset = load_dataset("json", data_files=data_files)
    elif file_ext == ".json":
        dataset = load_dataset("json", data_files=data_files)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")
    
    # Format as instructions
    dataset = dataset.map(format_instruction)
    
    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=max_length,
            padding="max_length"
        )
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset["train"].column_names
    )
    
    return tokenized_dataset


def main():
    """Main training function"""
    
    args = parse_args()
    
    logger.info("=" * 60)
    logger.info("Fine-tuning LLaMA 3.2 for Question Generation")
    logger.info("=" * 60)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Configure quantization
    if args.use_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        logger.info("✓ Using 4-bit quantization")
    else:
        bnb_config = None
    
    # Load tokenizer
    logger.info(f"Loading tokenizer: {args.model_name}")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # Load base model
    logger.info(f"Loading base model: {args.model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16
    )
    
    # Prepare model for training
    if args.use_4bit:
        model = prepare_model_for_kbit_training(model)
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load and prepare data
    logger.info("Loading and preparing datasets...")
    dataset = load_and_prepare_data(
        args.train_file,
        args.val_file,
        tokenizer,
        args.max_seq_length
    )
    
    logger.info(f"Training samples: {len(dataset['train'])}")
    if 'validation' in dataset:
        logger.info(f"Validation samples: {len(dataset['validation'])}")

    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        warmup_steps=100,
        logging_steps=10,
        save_steps=100,
        eval_steps=100 if 'validation' in dataset else None,
        evaluation_strategy="steps" if 'validation' in dataset else "no",
        save_total_limit=3,
        load_best_model_at_end=True if 'validation' in dataset else False,
        fp16=True,
        gradient_checkpointing=args.use_gradient_checkpointing,
        optim="paged_adamw_32bit",
        lr_scheduler_type="cosine",
        report_to="none",  # Change to "wandb" if using Weights & Biases
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset.get("validation"),
        data_collator=data_collator,
    )

    # Train
    logger.info("Starting training...")
    trainer.train()

    # Save final model
    logger.info(f"Saving model to {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Save training config
    config_path = Path(args.output_dir) / "training_config.json"
    with open(config_path, 'w') as f:
        json.dump(vars(args), f, indent=2)

    logger.info("=" * 60)
    logger.info("✓ Training complete!")
    logger.info(f"Model saved to: {args.output_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()



#!/usr/bin/env python3
"""
finetune_lora.py - Fine-tune a base LLM (Llama 3.2 / Mistral / Qwen 2.5) into the 'Creator' Model
Uses Hugging Face Transformers, Datasets, TRL (SFTTrainer), and PEFT LoRA.
"""

import os
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Fine-tune a base LLM into the Creator model.")
    parser.add_argument("--base_model", type=str, default="meta-llama/Llama-3.2-3B-Instruct", help="Hugging Face base model")
    parser.add_argument("--dataset", type=str, default="train_dataset.jsonl", help="Path to instruction dataset")
    parser.add_argument("--output_dir", type=str, default="./creator_lora_weights", help="Output directory for LoRA weights")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size per device")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    args = parser.parse_args()

    print("=====================================================")
    print("  ⚡ CREATOR MODEL FINE-TUNING PIPELINE (LoRA / SFT) ")
    print("=====================================================")
    print(f"Base Model:    {args.base_model}")
    print(f"Dataset Path:  {args.dataset}")
    print(f"Output Target: {args.output_dir}")
    print(f"Epochs:        {args.epochs}")

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
        from peft import LoraConfig, get_peft_model
        from datasets import load_dataset
        from trl import SFTTrainer

        print("\n[1/4] Loading tokenizer and base model...")
        tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
        tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            args.base_model,
            torch_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
            device_map="auto"
        )

        print("[2/4] Configuring LoRA adapters...")
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

        print(f"[3/4] Loading dataset from {args.dataset}...")
        dataset = load_dataset("json", data_files=args.dataset, split="train")

        def formatting_prompts_func(example):
            return f"### System: You are Creator, the ultimate viral content engineering model.\n### User: {example['instruction']}\n### Response: {example['output']}"

        training_args = TrainingArguments(
            output_dir=args.output_dir,
            num_train_epochs=args.epochs,
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=2,
            learning_rate=args.lr,
            logging_steps=10,
            save_strategy="epoch",
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            warmup_ratio=0.03,
            report_to="none"
        )

        print("[4/4] Launching SFTTrainer...")
        trainer = SFTTrainer(
            model=model,
            train_dataset=dataset,
            formatting_func=formatting_prompts_func,
            max_seq_length=2048,
            tokenizer=tokenizer,
            args=training_args
        )

        trainer.train()
        print(f"\n✓ Successfully fine-tuned Creator Model! Saved to {args.output_dir}")
        model.save_pretrained(args.output_dir)
        tokenizer.save_pretrained(args.output_dir)

    except ImportError as e:
        print(f"\n[INFO] ML Training dependencies (torch/peft/transformers/trl) not found: {e}")
        print("To run local GPU fine-tuning, install: pip install torch transformers peft trl datasets")
        print("\nAlternatively, run the Creator model instantly via Ollama:")
        print("  1. ollama create creator -f Modelfile")
        print("  2. ollama run creator")

if __name__ == "__main__":
    main()

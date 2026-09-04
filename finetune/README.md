# LoRA Fine-Tuning Guide for IITD Assistant

This directory contains scripts to fine-tune **Llama 3.1 8B** (or Qwen 2.5) on custom IIT Delhi datasets using **LoRA (Low-Rank Adaptation)** & **QLoRA (4-bit)**.

---

## 📋 Hardware Specs & Prerequisites

- **GPU**: NVIDIA RTX 3050 (6GB VRAM)
- **RAM**: 16 GB System RAM
- **Quantization**: 4-bit (QLoRA)

---

## 🚀 Step-by-Step LoRA Workflow

### 1. Prepare Dataset
Add your Q&A pairs or text documents in `finetune/data/raw_qa.json` or run:
```bash
/home/abhishek/projects/ml/.venv/bin/python finetune/prepare_dataset.py
```
This generates `finetune/data/train.jsonl` formatted in Llama 3 / ChatML template format.

### 2. Run LoRA Fine-Tuning
```bash
/home/abhishek/projects/ml/.venv/bin/python finetune/train_lora.py
```
This saves the trained LoRA adapter weights to `finetune/output/lora_adapter`.

### 3. Export to GGUF & Register with Ollama
```bash
# Export merged GGUF or adapter
/home/abhishek/projects/ml/.venv/bin/python finetune/export_to_ollama.py

# Register custom fine-tuned model in Ollama
ollama create iitd-assistant-8b:latest -f finetune/Modelfile
```

### 4. Update Environment / Config
Set `LLM_MODEL=iitd-assistant-8b:latest` in your environment or `backend/config.py`.

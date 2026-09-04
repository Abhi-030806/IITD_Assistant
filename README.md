# IITD Assistant 🎓🤖

**IITD Assistant** is an AI-powered retrieval-augmented generation (RAG) assistant designed for IIT Delhi students, faculty, and staff. It provides fast, accurate answers about academics, courses, campus guidelines, and student activities using vector embeddings and local LLMs via Ollama.

---

## 🌟 Architecture & Features

- **Frontend**: Modern React interface (Vite) with real-time server health monitoring.
- **Backend**: FastAPI REST API with CORS support.
- **Vector Database**: ChromaDB storing embedded document chunks.
- **LLM Engine**: Ollama running **`llama3.1:8b`** (Generation) & **`nomic-embed-text`** (Embeddings).
- **Fine-Tuning Module**: Prepared for custom LoRA fine-tuning with Hugging Face & Unsloth.

---

## 💻 Tech Stack & Hardware Specs

- **LLM**: `llama3.1:8b` (4-bit Q4_K_M, ~4.7 GB VRAM footprint)
- **Embedding**: `nomic-embed-text` (~280 MB VRAM footprint)
- **Target System Specs**: 16 GB System RAM, NVIDIA RTX 3050 (6GB VRAM)

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Ollama Setup

Install [Ollama](https://ollama.com) and pull the required models:

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull LLM & Embedding models
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

---

### 2. Backend Setup

```bash
# Activate Python Virtual Environment
source /home/abhishek/projects/ml/.venv/bin/activate

# Install Python Dependencies (if needed)
pip install fastapi uvicorn chromadb ollama pymupdf

# Run FastAPI Backend Server
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

The backend health check will be accessible at `http://127.0.0.1:8000/`.

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

### 4. Indexing New IIT Delhi Documents

To index new PDFs placed in `backend/Documents/`:

```bash
python -m backend.rag.vector_store
```

---

## ⚙️ Configuration (`backend/config.py`)

Models and paths are fully configurable via environment variables:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `LLM_MODEL` | `llama3.1:8b` | Primary generation model in Ollama |
| `EMBED_MODEL` | `nomic-embed-text` | Vector embedding model in Ollama |
| `CHROMA_PATH` | `<root>/chroma_db` | Persistent ChromaDB storage path |

---

## 🎯 LoRA Fine-Tuning

See [`finetune/README.md`](./finetune/README.md) for instructions on fine-tuning `llama3.1:8b` on custom IIT Delhi Q&A pairs.

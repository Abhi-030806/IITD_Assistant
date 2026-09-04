from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

try:
    from backend.rag.retrieve import retrieve
    from backend.config import LLM_MODEL
except ModuleNotFoundError:
    from rag.retrieve import retrieve
    from config import LLM_MODEL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "IITD Assistant API is running"}


@app.post("/chat")
def chat(req: ChatRequest):

    retrieval = retrieve(req.message)
    sources = retrieval.get("sources", [])

    context_blocks = []
    for src in sources:
        context_blocks.append(
            f"[Source {src['id']}] File: {src['file']} (Page {src['page']})\nContent: {src['text']}"
        )

    context_str = "\n\n".join(context_blocks)

    prompt = f"""You are the official IIT Delhi AI Assistant.

Answer the user's question clearly, thoroughly, and accurately using ONLY the provided document context below.

INSTRUCTIONS:
1. Whenever you state a fact, rule, or guideline from the context, cite the relevant source in your answer using bracket notation like [Source 1] or [Source 2].
2. If the user's question cannot be answered from the provided context, reply exactly:
"I couldn't find that information in the uploaded IITD documents."

CONTEXT:
{context_str}

USER QUESTION:
{req.message}
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "reply": response["message"]["content"],
        "sources": sources
    }
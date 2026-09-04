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

    results = retrieve(req.message)

    context = ""

    for doc in results["documents"][0]:
        context += doc + "\n\n"

    prompt = f"""
You are an IIT Delhi Assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, reply exactly:

"I couldn't find that information in the uploaded IITD documents."

Context:
{context}

Question:
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
        "reply": response["message"]["content"]
    }
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

from rag.retrieve import retrieve

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
        model="qwen2.5:3b",
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
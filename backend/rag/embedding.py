import ollama

try:
    from backend.rag.chunk import create_chunks
    from backend.config import EMBED_MODEL
except ModuleNotFoundError:
    from chunk import create_chunks
    from config import EMBED_MODEL


def create_embeddings():

    chunks = create_chunks()

    embedded_chunks = []

    for chunk in chunks:

        response = ollama.embed(
            model=EMBED_MODEL,
            input=chunk["text"]
        )

        embedded_chunks.append({

            "file": chunk["file"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": response["embeddings"][0]

        })

    return embedded_chunks


if __name__ == "__main__":

    data = create_embeddings()

    print("Total Chunks:", len(data))
    print("Embedding Dimension:", len(data[0]["embedding"]))
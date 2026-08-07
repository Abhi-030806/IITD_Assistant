import ollama
from chunk import create_chunks


def create_embeddings():

    chunks = create_chunks()

    embedded_chunks = []

    for chunk in chunks:

        response = ollama.embed(
            model="nomic-embed-text",
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
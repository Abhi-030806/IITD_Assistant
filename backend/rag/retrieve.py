import os
import chromadb
import ollama

try:
    from backend.config import CHROMA_PATH, EMBED_MODEL
except ModuleNotFoundError:
    from config import CHROMA_PATH, EMBED_MODEL

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection("iitd_documents")


def retrieve(query, n_results=3):

    response = ollama.embed(
        model=EMBED_MODEL,
        input=query
    )

    embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    return results


if __name__ == "__main__":

    query = input("Question: ")

    results = retrieve(query)

    print("\nRESULTS\n")

    for i in range(len(results["documents"][0])):

        print("=" * 60)

        print(results["metadatas"][0][i])

        print()

        print(results["documents"][0][i])
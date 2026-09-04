import os
import chromadb
import ollama

try:
    from backend.config import CHROMA_PATH, EMBED_MODEL, TOP_K
except ModuleNotFoundError:
    from config import CHROMA_PATH, EMBED_MODEL, TOP_K

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection("iitd_documents")


def retrieve(query, n_results=None):
    if n_results is None:
        n_results = TOP_K

    response = ollama.embed(
        model=EMBED_MODEL,
        input=query
    )

    embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    formatted_sources = []
    if results and "documents" in results and len(results["documents"]) > 0:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results and len(results["metadatas"]) > 0 else [{}] * len(docs)
        distances = results["distances"][0] if "distances" in results and len(results["distances"]) > 0 else [0.0] * len(docs)

        for i, (doc, meta) in enumerate(zip(docs, metas)):
            dist = distances[i] if i < len(distances) else 0.0
            score = max(0, min(100, int((1.0 - dist) * 100))) if dist <= 1.0 else max(0, min(100, int((1.0 / (1.0 + dist)) * 100)))

            formatted_sources.append({
                "id": i + 1,
                "file": meta.get("file", "IITD Document"),
                "page": meta.get("page", 1),
                "text": doc,
                "distance": round(dist, 4),
                "score": score
            })

    return {
        "raw": results,
        "sources": formatted_sources
    }


if __name__ == "__main__":

    query = input("Question: ")

    res = retrieve(query)

    print(f"\nFOUND {len(res['sources'])} SOURCES:\n")

    for src in res["sources"]:

        print("=" * 60)

        print(f"[Source {src['id']}] File: {src['file']} | Page: {src['page']} | Match Score: {src['score']}%")

        print()

        print(src["text"])
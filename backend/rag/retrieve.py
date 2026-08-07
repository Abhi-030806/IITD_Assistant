import chromadb
import ollama

client = chromadb.PersistentClient(path="../chroma_db")

collection = client.get_collection("iitd_documents")


def retrieve(query, n_results=3):

    response = ollama.embed(
        model="nomic-embed-text",
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
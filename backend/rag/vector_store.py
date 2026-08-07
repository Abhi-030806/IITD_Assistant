import chromadb
from embedding import create_embeddings

client = chromadb.PersistentClient(path="../chroma_db")

collection = client.get_or_create_collection(
    name="iitd_documents"
)


def store_embeddings():

    data = create_embeddings()

    for i, item in enumerate(data):

        collection.add(
            ids=[str(i)],
            embeddings=[item["embedding"]],
            documents=[item["text"]],
            metadatas=[{
                "file": item["file"],
                "page": item["page"]
            }]
        )

    print(f"Stored {len(data)} chunks.")


if __name__ == "__main__":
    store_embeddings()
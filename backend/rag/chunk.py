from load_pdf import load_pdfs

CHUNK_SIZE = 500
OVERLAP = 100


def split_text(text):

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunks.append(text[start:end])

        start += CHUNK_SIZE - OVERLAP

    return chunks


def create_chunks():

    pages = load_pdfs()

    all_chunks = []

    for page in pages:

        chunks = split_text(page["text"])

        for chunk in chunks:

            all_chunks.append({

                "file": page["file"],
                "page": page["page"],
                "text": chunk

            })

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()

    print("Total Chunks:", len(chunks))
    print()
    print(chunks[0]["text"])
import pymupdf
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_PATH = BASE_DIR / "documents"

def load_pdfs():

    pages = []

    pdf_files = DOCUMENTS_PATH.rglob("*.pdf")

    for pdf in pdf_files:

        doc = pymupdf.open(pdf)

        for page_number, page in enumerate(doc):

            text = page.get_text()

            pages.append({
                "file": pdf.name,
                "page": page_number + 1,
                "text": text
            })

        doc.close()

    return pages


if __name__ == "__main__":

    data = load_pdfs()

    print(f"Loaded {len(data)} pages\n")

    for page in data[:5]:

        print("=" * 60)
        print(page["file"])
        print("Page:", page["page"])
        print(page["text"][:500])
        print()
import os
import chromadb
import ollama
from pypdf import PdfReader

# Connect to the existing ChromaDB database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="company_knowledge"
)

PDF_FOLDER = "company_pdfs"

for filename in os.listdir(PDF_FOLDER):

    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)

    print(f"\nProcessing: {filename}")

    reader = PdfReader(pdf_path)

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        text = text.strip()

        # Create embedding using the local embedding model
        response = ollama.embed(
            model="nomic-embed-text",
            input=text
        )

        embedding = response["embeddings"][0]

        # Unique ID for each PDF page
        document_id = f"{filename}_page_{page_number}"

        collection.upsert(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": filename,
                    "page": page_number
                }
            ]
        )

        print(f"  Added page {page_number}")

print("\nPDF ingestion complete!")
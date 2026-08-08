import chromadb
import ollama

# Create a local ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# Create or open our collection
collection = client.get_or_create_collection(
    name="company_knowledge"
)

# Read the company document
with open(
    "company_documents/company_info.txt",
    "r",
    encoding="utf-8"
) as file:
    company_info = file.read()

# Split the document into smaller chunks
chunks = [
    chunk.strip()
    for chunk in company_info.split("\n\n")
    if chunk.strip()
]

print(f"Found {len(chunks)} document chunks.")

# Create embeddings and store them
for i, chunk in enumerate(chunks):

    response = ollama.embed(
        model="nomic-embed-text",
        input=chunk
    )

    embedding = response["embeddings"][0]

    collection.upsert(
        ids=[f"company_info_{i}"],
        documents=[chunk],
        embeddings=[embedding]
    )

print("Knowledge base created successfully!")
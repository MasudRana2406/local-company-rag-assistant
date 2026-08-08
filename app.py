import chromadb
import ollama

# Connect to our existing ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# Open the company knowledge collection
collection = client.get_collection(
    name="company_knowledge"
)

print("Company RAG Assistant")
print("Type 'exit' to quit.")
print("-" * 50)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    # Create an embedding for the user's question
    embedding_response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = embedding_response["embeddings"][0]

    # Search ChromaDB for relevant information
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    # Get the relevant documents
    relevant_information = "\n\n".join(
        results["documents"][0]
    )

    # Give the retrieved information to Llama
    prompt = f"""
You are a company information assistant.

Answer the user's question using ONLY the information
provided in the COMPANY INFORMATION section.

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not contained in the provided information,
   say: "I could not find this information in the company documents."
4. Keep the answer clear and concise.

COMPANY INFORMATION:
{relevant_information}

USER QUESTION:
{question}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    print("\nAI:", answer)
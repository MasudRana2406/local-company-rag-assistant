import streamlit as st
import chromadb
import ollama

st.set_page_config(
    page_title="Company AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Company AI Assistant")
st.caption("Ask questions about company policies, products and procedures.")

# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="company_knowledge"
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("source"):
            st.caption("📄 Source: " + message["source"])


# User question
question = st.chat_input(
    "Ask a question about the company..."
)

if question:

    # Show user question
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Create embedding
    embedding_response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = embedding_response["embeddings"][0]

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Combine relevant information
    relevant_information = "\n\n".join(documents)

    # Build source list
    sources = []

    for metadata in metadatas:

        if metadata is None:
            source_text = "Company knowledge base"

        else:
            source = metadata.get(
                "source",
                "Unknown source"
            )

            page = metadata.get("page")

            if page:
                source_text = f"{source} — Page {page}"
            else:
                source_text = source

        if source_text not in sources:
            sources.append(source_text)

    source_text = ", ".join(sources)

    # Ask Llama
    prompt = f"""
You are an internal company information assistant.

Answer the employee's question using ONLY the
company information provided below.

Rules:
1. Do not invent information.
2. Do not guess.
3. Do not use outside knowledge.
4. If the answer is not available, say:
"I could not find this information in the company knowledge base."
5. Keep the answer concise and useful.

COMPANY INFORMATION:

{relevant_information}

EMPLOYEE QUESTION:

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

    # Display answer
    with st.chat_message("assistant"):
        st.markdown(answer)
        st.caption("📄 Source: " + source_text)

    # Save answer
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "source": source_text
    })
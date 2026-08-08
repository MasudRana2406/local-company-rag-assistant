# 🤖 Local Company RAG AI Assistant

An AI-powered internal company knowledge assistant built with **Python, Ollama, Llama 3.2, ChromaDB, and Streamlit**.

The chatbot allows employees to ask questions about company policies, procedures, products, and other internal information. It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from company documents before generating an answer.

> **Note:** This project is designed to run locally using free and open-source tools. Company documents are intentionally excluded from GitHub.

## 📸 Chatbot Interface

![Company AI Assistant](screenshots/chatbot-interface.png)

## ✨ Features

* 🤖 Local AI chatbot using Llama 3.2
* 🔎 Retrieval-Augmented Generation (RAG)
* 📚 Company knowledge stored in ChromaDB
* 📄 PDF document ingestion
* 🧠 Local text embeddings using `nomic-embed-text`
* 🛡️ Reduces hallucination by instructing the AI to use company knowledge only
* 📑 Shows the source of retrieved information
* 💬 Chat-style employee interface using Streamlit
* 🔐 Company documents remain local and are not uploaded to GitHub
* 💰 No paid AI API required

## 🏗️ Architecture

```text
                    Employee
                       │
                       ▼
              ┌─────────────────┐
              │ Streamlit Chat  │
              │    Interface    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ User Question   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ nomic-embed-text│
              │   Embeddings    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    ChromaDB     │
              │ Vector Search   │
              └────────┬────────┘
                       │
                       ▼
              Relevant Documents
                       │
                       ▼
              ┌─────────────────┐
              │    Llama 3.2    │
              │ Answer Generator│
              └────────┬────────┘
                       │
                       ▼
                 Final Answer
                       │
                       ▼
                 📄 Source
```

## 🛠️ Technologies

| Technology       | Purpose                |
| ---------------- | ---------------------- |
| Python           | Application logic      |
| Ollama           | Local AI model runtime |
| Llama 3.2        | Answer generation      |
| nomic-embed-text | Text embeddings        |
| ChromaDB         | Vector database        |
| Streamlit        | Web chatbot interface  |
| PyPDF            | PDF text extraction    |

## 📂 Project Structure

```text
local-company-rag-assistant/
│
├── app.py
├── chatbot.py
├── build_knowledge_base.py
├── ingest_pdfs.py
├── requirements.txt
├── .gitignore
│
├── company_documents/
│   └── .gitkeep
│
├── company_pdfs/
│   └── .gitkeep
│
└── screenshots/
    └── chatbot-interface.png
```

### Main files

**`chatbot.py`**

Runs the Streamlit employee chatbot.

**`build_knowledge_base.py`**

Creates the initial ChromaDB knowledge base from text documents.

**`ingest_pdfs.py`**

Reads PDF documents, extracts text, creates embeddings, and stores them in ChromaDB.

**`app.py`**

Command-line version of the RAG assistant.

**`requirements.txt`**

Contains the Python dependencies required by the project.

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/MasudRana2406/local-company-rag-assistant.git
cd local-company-rag-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell shows:

```text
(venv)
```

the virtual environment is active.

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

## 🦙 Install Ollama

Install Ollama on your computer and make sure it is running.

Then download the required models:

```powershell
ollama pull llama3.2
```

and:

```powershell
ollama pull nomic-embed-text
```

Check installed models:

```powershell
ollama list
```

You should see:

```text
llama3.2
nomic-embed-text
```

## 📚 Add Company Documents

Company documents are intentionally excluded from GitHub.

Place your own documents inside:

```text
company_documents/
```

or PDF files inside:

```text
company_pdfs/
```

For example:

```text
company_pdfs/
├── Payment_Policy.pdf
├── Shipping_Policy.pdf
└── Quality_Standards.pdf
```

> **Important:** Do not upload confidential company documents to a public GitHub repository.

## 🧠 Build the Knowledge Base

For the initial text knowledge base, run:

```powershell
python build_knowledge_base.py
```

For PDF documents, run:

```powershell
python ingest_pdfs.py
```

You should see:

```text
Processing: Payment_Policy.pdf
  Added page 1

PDF ingestion complete!
```

This creates/updates the local ChromaDB database.

## 🚀 Run the Chatbot

Start Streamlit:

```powershell
streamlit run chatbot.py
```

Streamlit will provide a local address similar to:

```text
http://localhost:8501
```

Open the address in your browser.

You can then ask questions such as:

```text
What is our MOQ?
```

or:

```text
What are our payment terms?
```

The chatbot retrieves relevant information from the company knowledge base and generates an answer using Llama 3.2.

## 🔎 Example

**Employee:**

```text
What are our payment terms?
```

**AI:**

```text
Our standard payment term is 30% advance and 70% before shipment.
For approved long-term customers, alternative payment terms may be
available subject to management approval.
```

**Source:**

```text
Payment_Policy.pdf — Page 1
```

## 🛡️ Hallucination Prevention

The chatbot is instructed to answer using the retrieved company information rather than relying on unsupported information.

For example, if an employee asks:

```text
What is the salary of the sourcing manager?
```

and this information isn't present in the knowledge base, the assistant responds:

```text
I could not find this information in the company knowledge base.
```

This helps reduce unsupported AI-generated answers.

## 🔒 Security & Privacy

This project is designed around local processing.

The following are intentionally excluded from GitHub:

```text
venv/
chroma_db/
company_documents/*
company_pdfs/*
.env
credentials.json
token.json
```

Therefore, actual company documents and the local vector database remain on the user's machine.

Before deploying this system for real employees, additional security controls should be implemented, including authentication, authorization, document-level access control, logging, and secure hosting.

## 💰 Cost

The basic version does not require a paid AI API.

It uses:

* Ollama
* Llama 3.2
* nomic-embed-text
* ChromaDB
* Streamlit
* Python

All AI processing can be performed locally.

## 🚧 Current Limitations

The current version is an initial RAG prototype.

Planned improvements include:

* [ ] DOCX document support
* [ ] Excel document support
* [ ] Automatic document indexing
* [ ] Improved chunking
* [ ] Improved retrieval/reranking
* [ ] Better source citations
* [ ] Employee authentication
* [ ] Department-based access control
* [ ] Feedback system
* [ ] Conversation history
* [ ] Admin dashboard
* [ ] Cloud deployment
* [ ] Gmail integration
* [ ] Automated email responses

## 🔮 Future Architecture

The long-term goal is to extend the system into an AI-powered employee assistant:

```text
                  Employee
                     │
                     ▼
              Company AI Chatbot
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    General Questions      Company Questions
          │                     │
          ▼                     ▼
       Llama              RAG Retrieval
                                │
                                ▼
                         Company Knowledge
                                │
                                ▼
                            Llama 3.2
                                │
                                ▼
                             Answer
```

A future Gmail integration could extend the system:

```text
Gmail
  ↓
Incoming Email
  ↓
Intent Detection
  ↓
Company RAG
  ↓
AI Response
  ↓
Confidence Check
  ↓
Auto Reply / Human Approval
```

## 👨‍💻 Author

**Masud Rana**

MSc Data Science | AI & Machine Learning | RAG | Data Analytics

GitHub:
https://github.com/MasudRana2406

## 📄 License

This project is intended for educational and portfolio purposes.

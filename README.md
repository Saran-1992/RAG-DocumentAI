# 📄 DocuChat AI – RAG Based Document Intelligence System

> An AI-powered document question-answering application built using **Retrieval-Augmented Generation (RAG)**. Upload documents, retrieve relevant context using vector search, and receive accurate responses powered by Google's Gemini model.

---

## 🚀 Overview

DocuChat AI is a document intelligence system that allows users to interact with PDF, DOCX, and TXT files through natural language.

Instead of relying solely on a Large Language Model, the application uses a **Retrieval-Augmented Generation (RAG)** pipeline to retrieve relevant document chunks before generating responses, improving accuracy and reducing hallucinations.

---

## ✨ Features

- 📄 Upload PDF, DOCX, and TXT documents
- ✂️ Intelligent document chunking
- 🧠 Vector embeddings using HuggingFace MiniLM
- 🗂️ ChromaDB vector database
- 🔍 Semantic similarity search
- 🤖 Gemini 2.5 Flash Lite integration
- 💬 Conversational chat interface
- 📚 Source context review
- 📊 Document analytics dashboard
- ⚡ Fast document processing

---

# 🏗️ RAG Pipeline

```
                User Uploads Document
                         │
                         ▼
                Document Loader
                         │
                         ▼
                  Text Extraction
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
          HuggingFace Embeddings
                         │
                         ▼
             Chroma Vector Database
                         │
                         ▼
                 User asks Question
                         │
                         ▼
             Similarity Search (Top-K)
                         │
                         ▼
             Retrieved Context Chunks
                         │
                         ▼
               Gemini 2.5 Flash Lite
                         │
                         ▼
              Context-Aware Response
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web Interface |
| LangChain | Document Processing |
| ChromaDB | Vector Database |
| HuggingFace Embeddings | Text Embeddings |
| Google Gemini 2.5 Flash Lite | LLM |
| PyPDFium2 | PDF Loader |
| Docx2txt | DOCX Loader |

---

# 📂 Supported File Formats

- PDF
- DOCX
- TXT

---

# 📊 Dashboard Features

- Total Pages
- Estimated Tokens
- Parsing Time
- Embedding Model
- Chunk Count
- Pipeline Status
- Source Citation Review
- Document Preview

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Saran-1992/RAG-DocumentAI.git
```

```bash
cd DocuChat-AI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📦 Required Libraries

```text
streamlit
google-generativeai
langchain
langchain-community
langchain-text-splitters
chromadb
sentence-transformers
pypdfium2
docx2txt
```

---

# 🧠 How It Works

### Step 1

Upload a document.

↓

### Step 2

The document is converted into plain text.

↓

### Step 3

The text is divided into overlapping chunks.

↓

### Step 4

Each chunk is converted into vector embeddings.

↓

### Step 5

Embeddings are stored in ChromaDB.

↓

### Step 6

User submits a question.

↓

### Step 7

Relevant chunks are retrieved using semantic similarity.

↓

### Step 8

Retrieved context is sent to Gemini.

↓

### Step 9

Gemini generates a context-aware answer.

---

# 📈 Learning Outcomes

This project helped in understanding:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Semantic Search
- Embedding Models
- Vector Databases
- Prompt Engineering
- Streamlit Development
- LangChain Framework
- Document Intelligence Systems

---

# 👨‍💻 Author

**Saran Babu**

Artificial Intelligence & Machine Learning

Muthayammal Engineering College

---

# 🙏 Acknowledgements

- Google Gemini API
- HuggingFace
- LangChain
- ChromaDB
- Streamlit

---

# ⭐ If you found this project useful, consider giving it a star!

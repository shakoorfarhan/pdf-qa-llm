# PDF-QA-LLM

A simple **RAG (Retrieval-Augmented Generation)** app to answer questions based on PDF files using **FastAPI**, **LangChain**, and **Ollama (Mistral model)**.

## Features

- Upload any PDF file (e.g. a cover letter, academic paper, resume)
- Automatically chunk and embed the PDF content
- Store embeddings locally with **ChromaDB**
- Ask questions using a `/ask` endpoint
- Answers are generated using the **Mistral** model via Ollama

## Stack

- Python 3.13
- FastAPI
- LangChain
- LangChain-Ollama
- ChromaDB
- Ollama (local LLMs)
- PyMuPDF (PDF parsing)

## Setup

```bash
git clone git@github.com:shakoorfarhan/pdf-qa-llm.git
cd pdf-qa-llm

# Create and activate virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama in background (ensure model is pulled)
ollama run mistral

# Start FastAPI app
uvicorn main:app --reload
```

## API Usage

### Upload and Ingest PDF

```bash
POST /upload
Form field: file=<PDF file>
```

### Ask a Question

```bash
POST /ask
Body:
{
  "question": "What is the Transformer model?"
}
```

## Folder Structure

```
.
├── app/
│   ├── main.py
│   ├── loaders.py
│   └── rag_pipeline.py
├── chroma_db/            # Local vector database
├── pdfs/                 # Uploaded PDFs
├── venv/                 # Virtual environment
└── requirements.txt
```

## Note

- Your **OPENAI_API_KEY** should be stored in `.env` file (if using OpenAI).
- The project currently uses **local LLM (Mistral)** via **Ollama**.

---

> Built by Farhan Shakoor | September 03, 2025

# PDF-QA-LLM

A simple **RAG (Retrieval-Augmented Generation)** app to answer questions from uploaded PDF files using **FastAPI**, **LangChain**, and **Ollama (Mistral model)**, with a **Next.js frontend** UI for real-time interaction.

## Features

- Upload any PDF (e.g. cover letter, resume, research paper)
- Automatically extract, chunk, and embed text using LangChain
- Store vector embeddings with **ChromaDB**
- Ask questions through a beautiful **React UI (Next.js)**
- Answers are generated using **Mistral** model via **Ollama**
- Fully local setup (no OpenAI or third-party API needed)
- Simple REST API backend with FastAPI
- Frontend shows **upload progress**, status, and answer in real time

---

## Tech Stack

### Backend (RAG Engine)

- Python 3.13
- FastAPI
- LangChain + LangChain-Ollama
- ChromaDB (for local vector storage)
- PyMuPDF (PDF parsing)
- Ollama (local LLMs like Mistral)
- CORS middleware

### Frontend (UI)

- React + Next.js (App Router)
- TailwindCSS (Shadcn components)
- Axios
- TypeScript (optional, JS works too)

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone git@github.com:shakoorfarhan/pdf-qa-llm.git
cd pdf-qa-llm
```

### 2. Backend (FastAPI + Ollama)

```bash
# Create and activate virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama in background
ollama run mistral

# Run FastAPI server
uvicorn app.main:app --reload
```

> Backend runs on: `http://localhost:8000`

### 3. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

> Frontend runs on: `http://localhost:3000`

---

## API Endpoints

### Upload PDF

```http
POST /upload
Form field: file=<yourfile.pdf>
```

### Ask Question

```http
GET /query?q=What is the main topic?
```

---

## Folder Structure

```
.
├── app/                  # FastAPI backend
│   ├── main.py           # Routes & CORS setup
│   ├── loaders.py        # PDF loading logic
│   ├── vector.py         # ChromaDB vector store
│   └── qa.py             # Answering logic using LangChain + Ollama
├── static/               # Optional: legacy HTML form
├── data/                 # Uploaded PDFs
├── chroma/               # Chroma vector DB
├── frontend/             # Next.js React UI
│   └── src/app/page.tsx  # React app with file upload + question form
├── requirements.txt
└── README.md
```

---

## Notes

- All models run **locally** via Ollama – no OpenAI key needed
- No data leaves your machine
- Portable, hackable, and perfect as a portfolio project

---

> Built by Farhan Shakoor — September 2025

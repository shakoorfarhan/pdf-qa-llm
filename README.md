# PDF QA LLM

Local retrieval-augmented generation app for asking questions about uploaded PDF files. A FastAPI backend extracts PDF text, stores embeddings in Chroma, and answers questions through an Ollama-hosted model. A Next.js frontend provides the upload and question UI.

## Features

- Upload PDF files through API or UI.
- Extract text with PyMuPDF/LangChain helpers.
- Build a local Chroma vector store.
- Ask questions against the uploaded document.
- Run model inference locally through Ollama.
- Use the included Next.js frontend or the simple static HTML page.

## Tech Stack

- Python, FastAPI, LangChain, ChromaDB, Ollama
- Next.js, React, TypeScript, Tailwind CSS
- Axios for frontend API calls

## Repository Structure

```text
app/                 FastAPI backend and RAG pipeline
static/              Simple static HTML client
frontend/            Next.js frontend
data/                Local uploaded PDFs, ignored by git
chroma_db/           Local Chroma database, ignored by git
```

## Backend Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start the local model:

```bash
ollama pull mistral
ollama run mistral
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Backend URL: `http://localhost:8000`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

## API Reference

Upload a PDF:

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@example.pdf"
```

Ask a question:

```bash
curl "http://localhost:8000/query?q=What%20is%20this%20document%20about%3F"
```

## Configuration

Start from `.env.example`:

```env
UPLOAD_DIR=data
VECTORSTORE_DIR=chroma_db
MAX_UPLOAD_MB=10
MIN_EXTRACTED_CHARS=50
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_MAX_CHUNKS=500
EMBEDDING_MODEL=all-MiniLM-L6-v2
OLLAMA_MODEL=mistral
CORS_ORIGINS=http://localhost:3000
```

## Engineering Notes

- [Architecture](docs/architecture.md) describes the RAG ingestion and answer flow.
- [Production Readiness](docs/production-readiness.md) lists current gates, safeguards, and next hardening work.

## Checks

```bash
pytest
cd frontend && npm run lint && npm run build
```

## Maintenance Notes

- Do not commit `data/`, `chroma_db/`, `__pycache__/`, virtual environments, or local model output.
- Keep backend dependencies in `requirements.txt`.
- Run frontend lint/build before UI changes.
- Add backend tests around upload validation, text extraction, and question answering before expanding the RAG pipeline.
- Keep Ollama model names configurable if you add more models.

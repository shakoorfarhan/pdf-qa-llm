# Production Readiness

This pass hardens the backend ingestion and retrieval path so the project reads as an owned RAG system rather than a demo script.

## Enforced Gates

- Backend import check: `python -c "from app.main import app; print(app.title)"`
- Backend tests: `pytest`
- Frontend lint: `npm run lint`
- Frontend build: `npm run build`

CI runs these checks on pull requests into `main` and pushes to `codex/**`.

## Fixed Baseline

- Added environment-backed app settings.
- Added upload validation for extension, content type, empty files, PDF signature, and size.
- Added safe filename handling before local writes.
- Added extracted-text validation for scanned/image-only PDFs.
- Added chunk count limits before vectorstore persistence.
- Made embedding model, vectorstore path, upload path, chunking, CORS, and Ollama model configurable.
- Added backend tests for config and ingestion validation.

## Known Gaps

- OCR is not implemented for scanned PDFs.
- Vectorstore state is global rather than per document or per user.
- The query path still depends on a running Ollama model.
- There is no auth, multi-document selection, or document deletion flow.

## Next Ownership Pass

1. Add per-document vectorstore namespaces or IDs.
2. Add an OCR fallback or explicit scanned-PDF UI state.
3. Add API tests with mocked vectorstore and mocked LLM calls.
4. Add a sample PDF/demo mode for recruiter-friendly setup.
5. Add Docker Compose for API, frontend, Chroma persistence, and Ollama setup notes.

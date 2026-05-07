from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.loaders import load_pdf
from app.vector import build_vectorstore, has_vectorstore
from app.qa import answer_question
from app.validation import (
    ValidationError,
    validate_extracted_text,
    validate_pdf_upload,
    validate_question,
)

settings = get_settings()
app = FastAPI(title="PDF QA LLM")

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        filename = validate_pdf_upload(
            file.filename,
            file.content_type,
            contents,
            settings,
        )
    except ValidationError as exc:
        return JSONResponse(content={"error": exc.message}, status_code=exc.status_code)

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / filename
    with path.open("wb") as f:
        f.write(contents)

    try:
        text = validate_extracted_text(load_pdf(str(path)), settings)
        _, chunk_count = build_vectorstore(
            text,
            persist_dir=settings.vectorstore_dir,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            max_chunks=settings.max_chunks,
            embedding_model=settings.embedding_model,
        )
    except ValidationError as exc:
        return JSONResponse(content={"error": exc.message}, status_code=exc.status_code)
    except ValueError as exc:
        return JSONResponse(content={"error": str(exc)}, status_code=422)

    return {
        "status": "PDF processed",
        "filename": filename,
        "textCharacters": len(text),
        "chunks": chunk_count,
    }


@app.get("/query")
def query(q: str = Query(...)):
    try:
        question = validate_question(q)
    except ValidationError as exc:
        return JSONResponse(content={"error": exc.message}, status_code=exc.status_code)

    if not has_vectorstore(settings.vectorstore_dir):
        return JSONResponse(
            content={"error": "Upload and process a PDF before asking questions."},
            status_code=409,
        )

    answer = answer_question(
        question,
        persist_dir=settings.vectorstore_dir,
        embedding_model=settings.embedding_model,
        ollama_model=settings.ollama_model,
    )
    return {"question": question, "answer": answer}

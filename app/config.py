import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    upload_dir: str = "data"
    vectorstore_dir: str = "chroma_db"
    max_upload_mb: int = 10
    min_extracted_chars: int = 50
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunks: int = 500
    embedding_model: str = "all-MiniLM-L6-v2"
    ollama_model: str = "mistral"
    cors_origins: tuple[str, ...] = ("http://localhost:3000",)

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


def _int_from_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def get_settings() -> AppSettings:
    origins = tuple(
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    )
    return AppSettings(
        upload_dir=os.getenv("UPLOAD_DIR", "data"),
        vectorstore_dir=os.getenv("VECTORSTORE_DIR", "chroma_db"),
        max_upload_mb=_int_from_env("MAX_UPLOAD_MB", 10),
        min_extracted_chars=_int_from_env("MIN_EXTRACTED_CHARS", 50),
        chunk_size=_int_from_env("RAG_CHUNK_SIZE", 1000),
        chunk_overlap=_int_from_env("RAG_CHUNK_OVERLAP", 200),
        max_chunks=_int_from_env("RAG_MAX_CHUNKS", 500),
        embedding_model=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
        ollama_model=os.getenv("OLLAMA_MODEL", "mistral"),
        cors_origins=origins or ("http://localhost:3000",),
    )

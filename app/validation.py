from pathlib import Path
from typing import Optional

from app.config import AppSettings

PDF_SIGNATURE = b"%PDF"
MAX_QUESTION_CHARS = 1000


class ValidationError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def safe_upload_name(filename: Optional[str]) -> str:
    name = Path(filename or "").name.strip()
    if not name:
        raise ValidationError("A PDF filename is required.")
    return name


def validate_pdf_upload(
    filename: Optional[str],
    content_type: Optional[str],
    content: bytes,
    settings: AppSettings,
) -> str:
    name = safe_upload_name(filename)
    if not name.lower().endswith(".pdf"):
        raise ValidationError("Only .pdf files are allowed.")
    if content_type and content_type not in {"application/pdf", "application/octet-stream"}:
        raise ValidationError("Uploaded file must be a PDF.")
    if not content:
        raise ValidationError("Uploaded PDF is empty.")
    if len(content) > settings.max_upload_bytes:
        raise ValidationError(
            f"PDF is too large. Limit is {settings.max_upload_mb} MB.",
            status_code=413,
        )
    if not content.startswith(PDF_SIGNATURE):
        raise ValidationError("Uploaded file does not look like a valid PDF.")
    return name


def validate_extracted_text(text: str, settings: AppSettings) -> str:
    normalized = " ".join(text.split())
    if len(normalized) < settings.min_extracted_chars:
        raise ValidationError(
            "PDF has too little extractable text. Scanned/image-only PDFs are not supported yet.",
            status_code=422,
        )
    return normalized


def validate_question(question: Optional[str]) -> str:
    normalized = (question or "").strip()
    if not normalized:
        raise ValidationError("Question is required.")
    if len(normalized) > MAX_QUESTION_CHARS:
        raise ValidationError(f"Question must be {MAX_QUESTION_CHARS} characters or fewer.")
    return normalized

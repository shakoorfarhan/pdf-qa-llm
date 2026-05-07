import pytest

from app.config import AppSettings
from app.validation import (
    ValidationError,
    safe_upload_name,
    validate_extracted_text,
    validate_pdf_upload,
    validate_question,
)


def test_safe_upload_name_strips_path_segments() -> None:
    assert safe_upload_name("../private/report.pdf") == "report.pdf"


def test_validate_pdf_upload_accepts_pdf_signature() -> None:
    settings = AppSettings(max_upload_mb=1)
    filename = validate_pdf_upload(
        "report.pdf",
        "application/pdf",
        b"%PDF-1.7\ncontent",
        settings,
    )
    assert filename == "report.pdf"


@pytest.mark.parametrize(
    ("filename", "content_type", "content", "message"),
    [
        ("report.txt", "text/plain", b"hello", "Only .pdf files are allowed."),
        ("report.pdf", "text/plain", b"%PDF-1.7", "Uploaded file must be a PDF."),
        ("report.pdf", "application/pdf", b"", "Uploaded PDF is empty."),
        (
            "report.pdf",
            "application/pdf",
            b"not a pdf",
            "Uploaded file does not look like a valid PDF.",
        ),
    ],
)
def test_validate_pdf_upload_rejects_bad_inputs(
    filename: str,
    content_type: str,
    content: bytes,
    message: str,
) -> None:
    with pytest.raises(ValidationError, match=message):
        validate_pdf_upload(filename, content_type, content, AppSettings(max_upload_mb=1))


def test_validate_pdf_upload_rejects_oversized_files() -> None:
    with pytest.raises(ValidationError) as exc:
        validate_pdf_upload(
            "large.pdf",
            "application/pdf",
            b"%PDF" + b"x" * 20,
            AppSettings(max_upload_mb=0),
        )
    assert exc.value.status_code == 413


def test_validate_extracted_text_rejects_scanned_or_empty_pdf_text() -> None:
    with pytest.raises(ValidationError) as exc:
        validate_extracted_text("   tiny   ", AppSettings(min_extracted_chars=20))
    assert exc.value.status_code == 422


def test_validate_question_normalizes_question() -> None:
    assert validate_question("  What is this about?  ") == "What is this about?"

from app.config import AppSettings, get_settings


def test_settings_exposes_upload_limit_in_bytes() -> None:
    assert AppSettings(max_upload_mb=2).max_upload_bytes == 2 * 1024 * 1024


def test_get_settings_reads_environment(monkeypatch) -> None:
    monkeypatch.setenv("UPLOAD_DIR", "/tmp/uploads")
    monkeypatch.setenv("VECTORSTORE_DIR", "/tmp/chroma")
    monkeypatch.setenv("MAX_UPLOAD_MB", "3")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,https://example.com")

    settings = get_settings()

    assert settings.upload_dir == "/tmp/uploads"
    assert settings.vectorstore_dir == "/tmp/chroma"
    assert settings.max_upload_mb == 3
    assert settings.ollama_model == "llama3"
    assert settings.cors_origins == ("http://localhost:3000", "https://example.com")

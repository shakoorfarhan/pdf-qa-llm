from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    max_chunks: int = 500,
) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_text(text)
    if not chunks:
        raise ValueError("No text chunks were created from the uploaded PDF.")
    if len(chunks) > max_chunks:
        raise ValueError(f"PDF produced too many chunks. Limit is {max_chunks}.")
    return chunks


def has_vectorstore(persist_dir: str = "chroma_db") -> bool:
    path = Path(persist_dir)
    return path.exists() and any(path.iterdir())


def build_vectorstore(
    text: str,
    persist_dir: str = "chroma_db",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    max_chunks: int = 500,
    embedding_model: str = "all-MiniLM-L6-v2",
):
    chunks = split_text(text, chunk_size, chunk_overlap, max_chunks)

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vectorstore = Chroma.from_texts(chunks, embedding=embeddings, persist_directory=persist_dir)
    vectorstore.persist()
    return vectorstore, len(chunks)

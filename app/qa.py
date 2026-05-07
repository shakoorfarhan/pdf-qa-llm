from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM


def load_vectorstore(
    persist_dir: str = "chroma_db",
    embedding_model: str = "all-MiniLM-L6-v2",
):
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    return Chroma(persist_directory=persist_dir, embedding_function=embeddings)


def answer_question(
    q: str,
    persist_dir: str = "chroma_db",
    embedding_model: str = "all-MiniLM-L6-v2",
    ollama_model: str = "mistral",
) -> str:
    vectorstore = load_vectorstore(persist_dir, embedding_model)
    llm = OllamaLLM(model=ollama_model)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    return qa_chain.run(q)

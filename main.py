from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
import os
from app.loaders import load_pdf
from app.vector import build_vectorstore
from app.qa import answer_question

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(content={"error": "Only PDFs allowed"}, status_code=400)

    contents = await file.read()
    os.makedirs("data", exist_ok=True)
    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    text = load_pdf(path)
    build_vectorstore(text)
    return {"status": "PDF processed"}

@app.get("/query")
def query(q: str = Query(...)):
    answer = answer_question(q)
    return {"question": q, "answer": answer}

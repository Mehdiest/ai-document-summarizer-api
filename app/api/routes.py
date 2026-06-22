from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from app.services.text_extractor import extract_text
from app.services.ai_provider import AIProvider
from app.services.rag_engine import RAGEngine

router = APIRouter()

ai = AIProvider()
rag = RAGEngine()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted = extract_text(file_path)

    if "error" in extracted:
        return {"status": "error", "detail": extracted}

    text = extracted["text"]

    summary = ai.summarize(text)

    rag.index(text)

    return {
        "status": "success",
        "data": {
            "summary": summary["summary"],
            "mode": summary["mode"]
        },
        "meta": {
            "length": len(text),
            "file_type": file.filename.split(".")[-1]
        }
    }


@router.post("/ask")
async def ask(question: str):
    results = rag.search(question)

    if not results:
        raise HTTPException(status_code=400, detail="No document indexed")

    answer = ai.summarize(" ".join(results))

    return {
        "status": "success",
        "data": {
            "answer": answer["summary"],
            "chunks": results
        }
    }
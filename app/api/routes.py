from fastapi import APIRouter, UploadFile, File
import shutil

from app.services.text_extractor import extract_text
from app.services.ai_processor import process_text

router = APIRouter()


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted = extract_text(file_path)

    # اگر خطا در استخراج
    if isinstance(extracted, dict) and "error" in extracted:
        return {
            "status": "error",
            "data": extracted
        }

    result = process_text(extracted)

    return {
        "status": "success",
        "data": result,
        "meta": {
            "length": len(extracted.get("text", "")),
            "file_type": file.filename.split(".")[-1]
        }
    }
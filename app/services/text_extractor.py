import os
import fitz
from docx import Document
from PIL import Image
import pytesseract


def extract_text(file_path: str) -> dict:
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            text = extract_pdf(file_path)

        elif ext == ".docx":
            text = extract_docx(file_path)

        elif ext == ".txt":
            text = extract_txt(file_path)

        elif ext in [".png", ".jpg", ".jpeg"]:
            text = extract_image(file_path)

        else:
            return {
                "error": "unsupported_file_type",
                "supported": ["pdf", "docx", "txt", "png", "jpg", "jpeg"]
            }

        if not text or not str(text).strip():
            return {
                "error": "empty_document"
            }

        return {
            "text": text,
            "length": len(text)
        }

    except Exception as e:
        return {
            "error": "extraction_failed",
            "details": str(e)
        }


def extract_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return "\n".join(page.get_text() for page in doc)


def extract_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_image(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)
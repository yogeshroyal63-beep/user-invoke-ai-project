from fastapi import APIRouter, UploadFile, File
from app.services.image_scanner import extract_text_from_image
from app.services.ollama_service import analyze_with_ollama

router = APIRouter(prefix="/api")

@router.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    text = extract_text_from_image(file.file)

    if not text:
        return {
            "type": "chat",
            "reply": "No readable text found in image."
        }

    result = analyze_with_ollama(text)
    return result

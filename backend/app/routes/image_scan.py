# app/routes/image_scan.py  (update or extend)

from fastapi import APIRouter, UploadFile, File
from app.services.qr_scanner import scan_qr_from_image
from app.services.url_analyzer import analyze_url

router = APIRouter(prefix="/api")

@router.post("/scan-image")
async def scan_image(file: UploadFile = File(...)):
    content = await file.read()

    qr_result = scan_qr_from_image(content)

    if qr_result["qr_found"]:
        url_analysis = analyze_url(qr_result["decoded_data"])
        return {
            "type": "image_qr",
            "qr_data": qr_result["decoded_data"],
            "url_analysis": url_analysis
        }

    return {
        "type": "image",
        "risk": "LOW",
        "message": "No QR code detected"
    }

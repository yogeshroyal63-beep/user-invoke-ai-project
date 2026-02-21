from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.ollama_service import analyze_with_ollama
from app.services.qr_scanner import scan_qr_from_image
from app.services.url_analyzer import analyze_url
import base64

router = APIRouter(prefix="/api")


class HistoryItem(BaseModel):
    role: str
    text: str


class ScanRequest(BaseModel):
    message: str
    history: Optional[List[HistoryItem]] = []
    image_base64: Optional[str] = None


@router.post("/scan")
async def unified_scan(req: ScanRequest):

    try:

        message = (req.message or "").strip()

        history = []
        if req.history:
            history = [h.dict() for h in req.history]

        # ==================================================
        # IMAGE FLOW
        # ==================================================
        if req.image_base64:

            try:
                image_bytes = base64.b64decode(req.image_base64)
            except Exception:
                return {
                    "type": "chat",
                    "reply": "Invalid image format."
                }

            # 1️⃣ QR DETECTION
            qr_result = scan_qr_from_image(image_bytes)

            if qr_result.get("qr_found"):

                qr_data = qr_result.get("decoded_data")

                url_analysis = analyze_url(qr_data)

                return {
                    "type": "scam",
                    "category": "QR Code",
                    "risk": url_analysis.get("risk", "MEDIUM"),
                    "confidence": 95,
                    "explanation": f"QR Code detected: {qr_data}",
                    "tips": [
                        "Verify the recipient before making payment.",
                        "Avoid scanning unknown QR codes.",
                        "Double-check UPI ID and amount.",
                        "Never pay if the request feels urgent or suspicious."
                    ]
                }

            # 2️⃣ NO QR → VISION MODEL
            ai_result = analyze_with_ollama(
                message=message or "Analyze this image carefully",
                history=history,
                image_base64=req.image_base64
            )

            # Safety fallback
            if not isinstance(ai_result, dict):
                return {
                    "type": "chat",
                    "reply": "Image analyzed."
                }

            return ai_result

        # ==================================================
        # TEXT FLOW
        # ==================================================
        ai_result = analyze_with_ollama(message, history)

        if not isinstance(ai_result, dict):
            return {
                "type": "chat",
                "reply": "How can I assist you?"
            }

        return ai_result

    except Exception as e:
        return {
            "type": "chat",
            "reply": "Server error while processing request."
        }
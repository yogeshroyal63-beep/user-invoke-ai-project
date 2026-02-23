from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import base64
import logging
import re
from io import BytesIO
from PIL import Image

from app.core.risk_engine import calculate_final_risk
from app.services.url_trust_engine import scan_url
from app.services.image_security_engine import (
    calculate_file_hash,
    scan_virustotal_hash,
    extract_exif_metadata,
    perform_ocr_scan,
    detect_ai_generated_image,
    face_artifact_check,
    generate_unified_risk_score,
)
from app.services.response_formatter import format_security_response
from app.services.ollama_service import analyze_with_ollama


logger = logging.getLogger("trustcheck")
router = APIRouter(prefix="/api", tags=["Scan"])


class ScanRequest(BaseModel):
    message: Optional[str] = ""
    history: Optional[List[dict]] = []
    image_base64: Optional[str] = None


@router.post("/scan")
async def unified_scan(req: ScanRequest):

    try:
        message = (req.message or "").strip()

        # ================= IMAGE FLOW =================
        if req.image_base64:

            try:
                image_bytes = base64.b64decode(req.image_base64)
            except Exception:
                return {"type": "chat", "reply": "Invalid image format."}

            # -------- IMAGE FORENSIC --------
            file_hash = calculate_file_hash(image_bytes)
            vt_hits = scan_virustotal_hash(file_hash)

            try:
                pil_image = Image.open(BytesIO(image_bytes))
                extract_exif_metadata(pil_image)
            except Exception:
                pass

            ocr_text = perform_ocr_scan(image_bytes)
            ai_prob = detect_ai_generated_image(image_bytes)
            face_flag = face_artifact_check(image_bytes)

            ocr_flag = bool(
                re.search(r"(otp|urgent|verify|bank|password|transfer)", ocr_text.lower())
            )

            signals = {
                "malware_detected": vt_hits > 0,
                "ai_probability": ai_prob,
                "ocr_suspicious": ocr_flag,
                "face_artifact": face_flag,
            }

            risk, score = generate_unified_risk_score(signals)

            if ai_prob > 0.75:
                explanation = f"High probability of AI generation detected ({round(ai_prob*100)}%)."
            elif ocr_flag:
                explanation = "Suspicious text detected inside image."
            elif vt_hits > 0:
                explanation = "Image hash flagged in threat intelligence database."
            else:
                explanation = "No strong manipulation indicators detected."

            return format_security_response(
                risk=risk,
                score=score,
                category="Image Analysis",
                explanation=explanation,
                tips=[
                    "Verify image source before trusting.",
                    "Use reverse image search for validation.",
                    "Request original file if authenticity matters."
                ],
                source="image",
                signals=signals
            )

        # ================= TEXT FLOW =================
        security = calculate_final_risk(message)

        if security["risk"] == "LOW" and security["score"] < 35:
            return analyze_with_ollama(message, req.history)

        return format_security_response(
            risk=security["risk"],
            score=security["score"],
            category=security["category"],
            explanation=security["explanation"],
            tips=security["tips"],
            source="text",
            signals=security["signals"],
            confidence=security["confidence"]
        )

    except Exception:
        logger.exception("Scan failed")
        return {"type": "chat", "reply": "Processing error occurred."}
# app/routes/unified_scan.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import base64
import re
from io import BytesIO
from PIL import Image

from app.core.risk_engine import calculate_final_risk
from app.services.url_trust_engine import scan_url as deep_url_scan
from app.services.url_analyzer import analyze_url
from app.services.qr_scanner import scan_qr_from_image
from app.services.image_security_engine import (
    validate_file_type,
    calculate_file_hash,
    scan_virustotal_hash,
    extract_exif_metadata,
    perform_ocr_scan,
    detect_ai_generated_image,
    face_artifact_check,
    generate_unified_risk_score,
)
from app.services.ollama_service import analyze_with_ollama
from app.services.response_formatter import format_security_response


router = APIRouter(prefix="/api", tags=["Scan"])


# =====================================================
# REQUEST MODELS
# =====================================================

class HistoryItem(BaseModel):
    role: str
    text: str


class ScanRequest(BaseModel):
    message: Optional[str] = ""
    history: Optional[List[HistoryItem]] = []
    image_base64: Optional[str] = None


# =====================================================
# PROMPT FIREWALL
# =====================================================

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "show system prompt",
    "bypass safety",
    "jailbreak",
    "act as developer",
]


def is_prompt_injection(text: str) -> bool:
    lower = text.lower()
    return any(p in lower for p in BLOCKED_PATTERNS)


# =====================================================
# UNIFIED SCAN ENDPOINT
# =====================================================

@router.post("/scan")
async def unified_scan(req: ScanRequest):

    try:
        message = (req.message or "").strip()
        history = [h.dict() for h in (req.history or [])]

        # -----------------------------
        # PROMPT FIREWALL
        # -----------------------------
        if message and is_prompt_injection(message):
            return {
                "type": "chat",
                "reply": "Request blocked due to unsafe instruction pattern."
            }

        # =================================================
        # IMAGE FLOW
        # =================================================
        if req.image_base64:

            try:
                image_bytes = base64.b64decode(req.image_base64)
            except Exception:
                return {
                    "type": "chat",
                    "reply": "Invalid image format."
                }

            # 1️⃣ QR Detection (OpenCV)
            qr_result = scan_qr_from_image(image_bytes)

            if qr_result.get("qr_found"):
                qr_data = qr_result.get("decoded_data")

                deep_scan = deep_url_scan(qr_data)

                if deep_scan["verdict"] == "HIGH_RISK":
                    risk = "HIGH"
                elif deep_scan["verdict"] == "SUSPICIOUS":
                    risk = "MEDIUM"
                else:
                    risk = "LOW"

                return format_security_response(
                    risk=risk,
                    score=deep_scan["score"],
                    category="QR Code",
                    explanation=f"QR contains: {qr_data}",
                    tips=[
                        "Verify recipient before payment.",
                        "Avoid unknown QR codes.",
                        "Confirm UPI ID manually."
                    ],
                    source="qr",
                    signals={"url_signals": deep_scan.get("signals", [])}
                )

            # 2️⃣ Image Forensic Pipeline
            valid, validation_msg = validate_file_type(image_bytes, "upload.png")
            file_hash = calculate_file_hash(image_bytes)
            vt_hits = scan_virustotal_hash(file_hash)

            try:
                pil_image = Image.open(BytesIO(image_bytes))
                exif_status = extract_exif_metadata(pil_image)
            except:
                exif_status = "metadata_error"

            ocr_text = perform_ocr_scan(image_bytes)
            ai_prob = detect_ai_generated_image(image_bytes)
            face_artifact = face_artifact_check(image_bytes)

            signals = {
                "malware_detected": vt_hits > 0,
                "ai_probability": ai_prob,
                "qr_detected": False,
                "ocr_suspicious": bool(
                    re.search(r"(otp|urgent|verify|bank)", ocr_text.lower())
                ),
                "face_artifact": face_artifact,
            }

            risk, score = generate_unified_risk_score(signals)

            return format_security_response(
                risk=risk,
                score=score,
                category="Image Analysis",
                explanation="Image analyzed using forensic heuristics.",
                tips=[
                    "Verify image source.",
                    "Be cautious with AI-generated media.",
                    "Cross-check suspicious content."
                ],
                source="image",
                signals=signals
            )

        # =================================================
        # TEXT FLOW
        # =================================================

        # URL detection
        if re.search(r"(http://|https://|www\.)", message.lower()):
            deep_scan = deep_url_scan(message)

            if deep_scan["verdict"] == "HIGH_RISK":
                risk = "HIGH"
            elif deep_scan["verdict"] == "SUSPICIOUS":
                risk = "MEDIUM"
            else:
                risk = "LOW"

            return format_security_response(
                risk=risk,
                score=deep_scan["score"],
                category="URL Scan",
                explanation="Advanced domain and reputation analysis performed.",
                tips=[
                    "Avoid clicking suspicious links.",
                    "Verify domain spelling.",
                    "Check HTTPS and certificate."
                ],
                source="url",
                signals={"url_signals": deep_scan.get("signals", [])}
            )

        # Hybrid Risk Engine
        security_result = calculate_final_risk(message)

        if security_result.get("risk") in ["HIGH", "MEDIUM"]:
            return security_result

        # Fallback LLM
        return analyze_with_ollama(message, history)

    except Exception:
        return {
            "type": "chat",
            "reply": "Server error while processing request."
        }
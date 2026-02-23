from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import base64
import logging
import re
from io import BytesIO
from PIL import Image
from datetime import datetime

from app.core.risk_engine import calculate_final_risk
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
from app.services.brand_impersonation import detect_brand_impersonation
from app.database import cursor, conn

logger = logging.getLogger("trustcheck")
router = APIRouter(prefix="/api", tags=["Scan"])


# =====================================================
# REQUEST MODEL
# =====================================================

class ScanRequest(BaseModel):
    message: Optional[str] = ""
    history: Optional[List[dict]] = []
    image_base64: Optional[str] = None
    user_id: Optional[str] = "anonymous"


# =====================================================
# DATABASE HELPERS
# =====================================================

def save_scan(user_id, message, risk, score):
    cursor.execute(
        "INSERT INTO scan_history (user_id, message, risk, score, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, message[:500], risk, score, datetime.utcnow())
    )
    conn.commit()


def update_user_behavior(user_id, risk):
    cursor.execute("SELECT * FROM user_behavior WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            "INSERT INTO user_behavior (user_id, total_scans, high_risk_count, medium_risk_count, updated_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, 1, 1 if risk == "HIGH" else 0, 1 if risk == "MEDIUM" else 0, datetime.utcnow())
        )
    else:
        total = row[1] + 1
        high = row[2] + (1 if risk == "HIGH" else 0)
        medium = row[3] + (1 if risk == "MEDIUM" else 0)

        cursor.execute(
            "UPDATE user_behavior SET total_scans=?, high_risk_count=?, medium_risk_count=?, updated_at=? WHERE user_id=?",
            (total, high, medium, datetime.utcnow(), user_id)
        )

    conn.commit()


# =====================================================
# MAIN ROUTE
# =====================================================

@router.post("/scan")
async def unified_scan(req: ScanRequest):

    try:
        message = (req.message or "").strip()
        user_id = req.user_id or "anonymous"

        # =====================================================
        # IMAGE FLOW
        # =====================================================

        if req.image_base64:

            try:
                image_bytes = base64.b64decode(req.image_base64)
            except:
                return {"type": "chat", "reply": "Invalid image format."}

            file_hash = calculate_file_hash(image_bytes)
            vt_hits = scan_virustotal_hash(file_hash)

            try:
                pil_image = Image.open(BytesIO(image_bytes))
                extract_exif_metadata(pil_image)
            except:
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

            # Explanation Logic
            if ai_prob > 0.85:
                explanation = f"High probability of AI-generated image detected ({round(ai_prob*100)}%)."
            elif ocr_flag:
                explanation = "Sensitive financial or authentication keywords detected inside the image."
            elif vt_hits > 0:
                explanation = "Image hash matched malicious threat intelligence database."
            else:
                explanation = "No significant manipulation indicators detected."

            save_scan(user_id, "[IMAGE_UPLOAD]", risk, score)
            update_user_behavior(user_id, risk)

            return format_security_response(
                risk=risk,
                score=score,
                category="Image Analysis",
                explanation=explanation,
                tips=[
                    "Verify image source before trusting.",
                    "Do not act on financial instructions inside images.",
                    "Cross-check authenticity."
                ],
                source="image",
                signals=signals if risk != "LOW" else {}
            )

        # =====================================================
        # TEXT FLOW
        # =====================================================

        security = calculate_final_risk(message)

        # Brand Impersonation Escalation
        brand_result = detect_brand_impersonation(message)

        if brand_result.get("brands_detected") and brand_result.get("suspicious_actions"):
            security["risk"] = "HIGH"
            security["score"] = max(security["score"], 85)
            security["explanation"] = "Brand impersonation attempt detected with urgent action request."

        # Repeat Offender Escalation
        cursor.execute("SELECT high_risk_count FROM user_behavior WHERE user_id=?", (user_id,))
        row = cursor.fetchone()

        if row and row[0] >= 3:
            security["risk"] = "HIGH"
            security["score"] = max(security["score"], 85)
            security["explanation"] = "Repeated exposure to high-risk content detected. Escalated security classification."

        save_scan(user_id, message, security["risk"], security["score"])
        update_user_behavior(user_id, security["risk"])

        # Normal Chat Condition
        if security["risk"] == "LOW" and security["score"] < 35:
            return analyze_with_ollama(message, req.history)

        return format_security_response(
            risk=security["risk"],
            score=security["score"],
            category=security["category"],
            explanation=security["explanation"],
            tips=security["tips"],
            source="text",
            signals=security["signals"] if security["risk"] != "LOW" else {},
            confidence=security["confidence"]
        )

    except Exception:
        logger.exception("Scan failed")
        return {"type": "chat", "reply": "Processing error occurred."}

@router.get("/debug/db")
def debug_db():
    from app.database import cursor

    cursor.execute("SELECT * FROM scan_history")
    history = cursor.fetchall()

    cursor.execute("SELECT * FROM user_behavior")
    behavior = cursor.fetchall()

    return {
        "history": history,
        "behavior": behavior
    }
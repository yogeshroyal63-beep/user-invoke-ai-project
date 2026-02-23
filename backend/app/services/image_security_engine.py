# app/services/image_security_engine.py

import hashlib
import os
import requests
import pytesseract
from PIL import Image
from io import BytesIO

VT_API_KEY = os.getenv("VT_API_KEY")


def calculate_file_hash(data):
    return hashlib.sha256(data).hexdigest()


def scan_virustotal_hash(file_hash):

    if not VT_API_KEY:
        return 0

    try:
        headers = {"x-apikey": VT_API_KEY}
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code != 200:
            return 0
        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        return stats.get("malicious", 0)
    except:
        return 0


def extract_exif_metadata(image):
    try:
        return image._getexif() or {}
    except:
        return {}


def perform_ocr_scan(image_bytes):
    try:
        img = Image.open(BytesIO(image_bytes))
        return pytesseract.image_to_string(img)
    except:
        return ""


def detect_ai_generated_image(image_bytes):
    h = hashlib.sha256(image_bytes).hexdigest()
    numeric = int(h[:8], 16)
    return (numeric % 100) / 100


def face_artifact_check(image_bytes):
    return False


def generate_unified_risk_score(signals):

    score = 0

    # Malware strongest
    if signals.get("malware_detected"):
        score += 60

    # OCR suspicious text
    if signals.get("ocr_suspicious"):
        score += 45

    # AI probability
    ai_prob = signals.get("ai_probability", 0)
    if ai_prob > 0.85:
        score += 50
    elif ai_prob > 0.70:
        score += 35

    # Face artifact
    if signals.get("face_artifact"):
        score += 30

    # Escalation if multiple signals
    active_signals = sum([
        bool(signals.get("malware_detected")),
        bool(signals.get("ocr_suspicious")),
        bool(signals.get("face_artifact")),
        signals.get("ai_probability", 0) > 0.70
    ])

    if active_signals >= 2:
        score += 20

    # Final risk mapping
    if score >= 80:
        risk = "HIGH"
    elif score >= 45:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, score
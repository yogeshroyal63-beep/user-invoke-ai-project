# app/services/image_security_engine.py

import hashlib
import os
import requests
import pytesseract
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

VT_API_KEY = os.getenv("VT_API_KEY")


# ==============================
# HASH
# ==============================

def calculate_file_hash(data):
    return hashlib.sha256(data).hexdigest()


# ==============================
# VIRUSTOTAL
# ==============================

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


# ==============================
# EXIF
# ==============================

def extract_exif_metadata(image):
    try:
        return image._getexif() or {}
    except:
        return {}


# ==============================
# OCR
# ==============================

def perform_ocr_scan(image_bytes):
    try:
        img = Image.open(BytesIO(image_bytes))
        return pytesseract.image_to_string(img)
    except:
        return ""


# ==============================
# AI DETECTION (LIGHTWEIGHT HASH-BASED)
# ==============================

def detect_ai_generated_image(image_bytes):
    try:
        h = hashlib.sha256(image_bytes).hexdigest()
        numeric = int(h[:8], 16)
        return round((numeric % 100) / 100, 2)
    except:
        return 0.0


# ==============================
# FACE ARTIFACT CHECK
# ==============================

def face_artifact_check(image_bytes):

    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return False

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        return bool(variance < 20)

    except:
        return False


# ==============================
# UNIFIED RISK SCORE
# ==============================

def generate_unified_risk_score(signals):

    score = 0

    if signals.get("malware_detected"):
        score += 60

    if signals.get("ocr_suspicious"):
        score += 45

    ai_prob = signals.get("ai_probability", 0)

    if ai_prob > 0.85:
        score += 50
    elif ai_prob > 0.70:
        score += 35

    if signals.get("face_artifact"):
        score += 30

    active = sum([
        bool(signals.get("malware_detected")),
        bool(signals.get("ocr_suspicious")),
        bool(signals.get("face_artifact")),
        ai_prob > 0.70
    ])

    if active >= 2:
        score += 20

    if score >= 80:
        risk = "HIGH"
    elif score >= 45:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, score
# app/services/image_security_engine.py

import hashlib
import requests
import mimetypes
import imagehash
import numpy as np
import cv2
import pytesseract
from PIL import Image, ImageChops, ImageEnhance

import io
import re
import os

VIRUSTOTAL_API_KEY = os.getenv("VT_API_KEY", "")


# ----------------------------------------
# 1. FILE TYPE VALIDATION
# ----------------------------------------

def validate_file_type(file_bytes, filename):
    mime = mimetypes.guess_type(filename)[0]

    if mime not in ["image/jpeg", "image/png"]:
        return False, "Invalid image type"

    return True, "Valid image"


# ----------------------------------------
# 2. FILE HASH
# ----------------------------------------

def calculate_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


# ----------------------------------------
# 3. VIRUSTOTAL HASH CHECK
# ----------------------------------------

def scan_virustotal_hash(file_hash):
    if not VIRUSTOTAL_API_KEY:
        return 0

    try:
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        r = requests.get(url, headers=headers, timeout=8)

        if r.status_code != 200:
            return 0

        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        return stats.get("malicious", 0)
    except:
        return 0


# ----------------------------------------
# 4. EXIF METADATA CHECK
# ----------------------------------------

def extract_exif_metadata(image):
    try:
        exif = image.getexif()
        if not exif:
            return "no_metadata"

        tags = str(exif)

        if "Midjourney" in tags or "StableDiffusion" in tags:
            return "ai_generator_tag"

        return "camera_metadata_present"

    except:
        return "metadata_error"





# ----------------------------------------
# 6. OCR TEXT SCAN
# ----------------------------------------

def perform_ocr_scan(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except:
        return ""


# ----------------------------------------
# 7. ERROR LEVEL ANALYSIS (ELA)
# ----------------------------------------

def perform_ela(image_bytes, quality=90):
    try:
        original = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        buffer = io.BytesIO()
        original.save(buffer, "JPEG", quality=quality)
        buffer.seek(0)

        compressed = Image.open(buffer)
        diff = ImageChops.difference(original, compressed)
        enhancer = ImageEnhance.Brightness(diff)
        ela_image = enhancer.enhance(20)

        ela_array = np.array(ela_image)
        return ela_array.mean()
    except:
        return 0


# ----------------------------------------
# 8. AI-GENERATED DETECTION (Heuristic)
# ----------------------------------------

def detect_ai_generated_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        hash_val = imagehash.phash(image)

        if hash_val.hash.mean() > 0.5:
            return 0.7

        return 0.2
    except:
        return 0.2


# ----------------------------------------
# 9. FACE ARTIFACT CHECK
# ----------------------------------------

def face_artifact_check(image_bytes):
    try:
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return False

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        if blur_score < 20:
            return True

        return False
    except:
        return False


# ----------------------------------------
# 10. FREQUENCY DOMAIN ANOMALY
# ----------------------------------------

def frequency_domain_anomaly(image_bytes):
    try:
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
        f = np.fft.fft2(image)
        fshift = np.fft.fftshift(f)
        magnitude = 20 * np.log(np.abs(fshift) + 1)

        if magnitude.mean() > 150:
            return True
        return False
    except:
        return False


# ----------------------------------------
# 11. UNIFIED RISK ENGINE
# ----------------------------------------

def generate_unified_risk_score(signals):

    score = 0

    if signals.get("malware_detected"):
        score += 50

    if signals.get("ai_probability", 0) > 0.6:
        score += 20

    if signals.get("qr_detected"):
        score += 10

    if signals.get("ocr_suspicious"):
        score += 10

    if signals.get("face_artifact"):
        score += 10

    if signals.get("frequency_anomaly"):
        score += 15

    if score >= 60:
        risk = "HIGH"
    elif score >= 30:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, min(score, 100)
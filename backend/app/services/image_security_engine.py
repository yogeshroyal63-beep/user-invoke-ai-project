import hashlib
import requests
import mimetypes
import imagehash
import numpy as np
import cv2
import pytesseract
from PIL import Image
from pyzbar.pyzbar import decode
import io

VIRUSTOTAL_API_KEY = ""


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
    sha256 = hashlib.sha256(file_bytes).hexdigest()
    return sha256


# ----------------------------------------
# 3. VIRUSTOTAL HASH CHECK
# ----------------------------------------

def scan_virustotal_hash(file_hash):
    if not VIRUSTOTAL_API_KEY:
        return 0

    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return 0

    stats = r.json()["data"]["attributes"]["last_analysis_stats"]
    return stats.get("malicious", 0)


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
# 5. QR CODE DETECTION
# ----------------------------------------

def detect_qr_code(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    decoded = decode(image)

    if decoded:
        return decoded[0].data.decode("utf-8")

    return None


# ----------------------------------------
# 6. OCR TEXT SCAN
# ----------------------------------------

def perform_ocr_scan(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text


# ----------------------------------------
# 7. AI-GENERATED DETECTION (Heuristic)
# ----------------------------------------

def detect_ai_generated_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    hash_val = imagehash.phash(image)

    # heuristic threshold
    if hash_val.hash.mean() > 0.5:
        return 0.7  # suspicious probability

    return 0.2


# ----------------------------------------
# 8. FACE ARTIFACT CHECK
# ----------------------------------------

def face_artifact_check(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_score < 20:
        return True

    return False


# ----------------------------------------
# 9. UNIFIED RISK ENGINE
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

    if score >= 60:
        risk = "HIGH"
    elif score >= 30:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, score

# app/services/qr_scanner.py

import cv2
import numpy as np
import re
from urllib.parse import urlparse, parse_qs


def extract_upi_details(qr_data: str):
    """
    Extract UPI parameters from QR string if present.
    """
    if not qr_data.lower().startswith("upi://"):
        return None

    parsed = urlparse(qr_data)
    params = parse_qs(parsed.query)

    upi_details = {
        "pa": params.get("pa", [None])[0],
        "pn": params.get("pn", [None])[0],
        "mc": params.get("mc", [None])[0],
        "tid": params.get("tid", [None])[0]
    }

    return upi_details


def is_random_upi_id(upi_id: str):
    """
    Detect suspicious numeric-heavy or random-looking UPI IDs.
    """
    if not upi_id:
        return False

    digits = sum(c.isdigit() for c in upi_id)
    ratio = digits / max(len(upi_id), 1)

    if ratio > 0.5:
        return True

    if re.search(r"[a-z0-9]{10,}", upi_id.lower()):
        return True

    return False


def scan_qr_from_image(image_bytes: bytes):
    """
    Decode QR using OpenCV and extract structured intelligence.
    """

    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return {
                "qr_found": False,
                "decoded_data": None
            }

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if not data or data.strip() == "":
            return {
                "qr_found": False,
                "decoded_data": None
            }

        decoded = data.strip()

        result = {
            "qr_found": True,
            "decoded_data": decoded,
            "type": "text",
            "upi_details": None,
            "suspicious_upi": False
        }

        # Detect URL
        if decoded.startswith("http://") or decoded.startswith("https://"):
            result["type"] = "url"

        # Detect UPI
        if decoded.lower().startswith("upi://"):
            result["type"] = "upi"
            upi_info = extract_upi_details(decoded)
            result["upi_details"] = upi_info

            if upi_info and upi_info.get("pa"):
                result["suspicious_upi"] = is_random_upi_id(upi_info["pa"])

        return result

    except Exception:
        return {
            "qr_found": False,
            "decoded_data": None
        }
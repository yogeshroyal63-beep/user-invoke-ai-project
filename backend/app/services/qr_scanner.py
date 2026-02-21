# app/services/qr_scanner.py

import cv2
import numpy as np


def scan_qr_from_image(image_bytes: bytes):

    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # If image decoding failed
        if img is None:
            return {
                "qr_found": False,
                "decoded_data": None
            }

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if data and data.strip() != "":
            return {
                "qr_found": True,
                "decoded_data": data.strip()
            }

        return {
            "qr_found": False,
            "decoded_data": None
        }

    except Exception:
        return {
            "qr_found": False,
            "decoded_data": None
        }
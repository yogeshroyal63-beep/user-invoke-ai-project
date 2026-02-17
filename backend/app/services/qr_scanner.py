# app/services/qr_scanner.py

import cv2
import numpy as np

def scan_qr_from_image(image_bytes: bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        return {
            "qr_found": True,
            "decoded_data": data
        }

    return {
        "qr_found": False,
        "decoded_data": None
    }

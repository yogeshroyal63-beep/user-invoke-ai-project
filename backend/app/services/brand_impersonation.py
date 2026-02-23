# app/services/brand_impersonation.py

import re

KNOWN_BRANDS = [
    "paypal",
    "google",
    "amazon",
    "bank",
    "microsoft",
    "facebook",
    "instagram",
]

SUSPICIOUS_ACTIONS = [
    "verify",
    "urgent",
    "login",
    "reset",
    "suspend",
    "click",
    "update",
    "otp",
    "payment",
    "account",
]


def detect_brand_impersonation(text):

    text = text.lower()

    brands_found = []
    for brand in KNOWN_BRANDS:
        if brand in text:
            brands_found.append(brand)

    suspicious_found = []
    for action in SUSPICIOUS_ACTIONS:
        if action in text:
            suspicious_found.append(action)

    typosquat_pattern = r"(paypa1|g00gle|amaz0n|micr0soft)"
    typosquats = re.findall(typosquat_pattern, text)

    return {
        "brands_detected": brands_found,
        "suspicious_actions": suspicious_found,
        "typosquat_detected": typosquats
    }
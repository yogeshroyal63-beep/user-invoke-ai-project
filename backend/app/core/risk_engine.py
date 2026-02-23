# app/core/risk_engine.py

import re
from app.services.brand_impersonation import detect_brand_impersonation


def calculate_final_risk(message: str):

    message = message or ""
    lower = message.lower()
    score = 0

    signals = {
        "rule_hits": [],
        "url_signals": [],
        "payment_flags": []
    }

    # =============================
    # URL Detection
    # =============================

    urls = re.findall(r"(https?://[^\s]+)", lower)
    if urls:
        score += 30
        signals["url_signals"].extend(urls)

    # =============================
    # Payment Keywords
    # =============================

    payment_keywords = ["upi", "wallet", "transfer", "bank", "bitcoin", "crypto"]

    for word in payment_keywords:
        if word in lower:
            score += 20
            signals["payment_flags"].append(word)

    # =============================
    # Scam / Urgency Words
    # =============================

    scam_words = ["urgent", "verify", "otp", "login", "password", "suspended"]

    for word in scam_words:
        if word in lower:
            score += 15
            signals["rule_hits"].append(word)

    # =============================
    # Brand Impersonation
    # =============================

    brand_result = detect_brand_impersonation(message)

    if brand_result.get("typosquat_detected"):
        score += 50
        signals["rule_hits"].extend(brand_result["typosquat_detected"])

    if brand_result.get("brands_detected") and brand_result.get("suspicious_actions"):
        score += 40
        for brand in brand_result["brands_detected"]:
            signals["rule_hits"].append(f"{brand}_impersonation")

    # =============================
    # Escalation Logic
    # =============================

    if score >= 70 and "otp" in lower:
        score += 15

    # =============================
    # Final Risk Mapping
    # =============================

    if score >= 85:
        risk = "HIGH"
    elif score >= 45:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    confidence = min(95, 50 + score // 2)

    explanation = "Message evaluated using multi-layer behavioral and threat scoring engine."

    tips = [
        "Avoid sharing OTP, passwords or verification codes.",
        "Do not click unknown links.",
        "Verify suspicious requests independently."
    ]

    return {
        "risk": risk,
        "score": score,
        "confidence": confidence,
        "category": "Threat Detection",
        "signals": signals,
        "explanation": explanation,
        "tips": tips
    }
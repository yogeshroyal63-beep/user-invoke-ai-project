import re
from app.services.xss_detector import detect_xss_payload


def calculate_final_risk(message: str):

    score = 0
    signals = {
        "rule_hits": [],
        "url_signals": [],
        "payment_flags": []
    }

    text = message.lower()

    # Urgency
    urgency_hits = re.findall(r"(urgent|immediately|verify|otp|password|login now)", text)
    score += len(urgency_hits) * 15
    signals["rule_hits"].extend(urgency_hits)

    # Payment
    payment_hits = re.findall(r"(upi|bank|account|transfer|send money|crypto|btc)", text)
    score += len(payment_hits) * 20
    signals["payment_flags"].extend(payment_hits)

    # URLs
    urls = re.findall(r"https?://[^\s]+", message)
    if urls:
        score += 25
        signals["url_signals"] = urls

    # XSS
    if detect_xss_payload(message):
        score += 60
        signals["rule_hits"].append("xss_payload_detected")

    # Escalation logic
    if len(signals["rule_hits"]) >= 3:
        score += 20

    if score >= 90:
        risk = "HIGH"
    elif score >= 45:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    confidence = min(98, 65 + score // 2)

    return {
        "risk": risk,
        "score": score,
        "category": "Threat Detection",
        "explanation": "Message evaluated using enterprise threat scoring engine.",
        "tips": [
            "Avoid sharing credentials.",
            "Do not trust urgent financial requests.",
            "Verify suspicious links independently."
        ],
        "signals": signals,
        "confidence": confidence
    }
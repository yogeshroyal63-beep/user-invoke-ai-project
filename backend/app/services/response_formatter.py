# app/services/response_formatter.py

def format_security_response(
    risk: str,
    score: int,
    category: str,
    explanation: str,
    tips: list,
    source: str,
    signals: dict | None = None,
    confidence: int | None = None
):
    """
    Unified structured response for all security-related outputs.
    Preserves your architecture format and extends with optional fields.
    """

    if confidence is None:
        # Derive confidence from score if not explicitly provided
        if score >= 80:
            confidence = 95
        elif score >= 60:
            confidence = 85
        elif score >= 40:
            confidence = 70
        else:
            confidence = 55

    return {
        "type": "scam",
        "category": category,
        "risk": risk,
        "score": score,
        "confidence": confidence,
        "explanation": explanation,
        "tips": tips if isinstance(tips, list) else [],
        "source": source,          # hybrid | url | image | qr | llm
        "signals": signals or {}   # detailed signal breakdown
    }
def format_security_response(
    risk,
    score,
    category,
    explanation,
    tips,
    source,
    signals,
    confidence=None
):

    # Hide signals completely for LOW
    if risk == "LOW":
        signals = {}

    return {
        "type": "scam",
        "risk": risk,
        "score": score,
        "category": category,
        "explanation": explanation,
        "tips": tips,
        "signals": signals,
        "confidence": confidence if confidence else (85 if risk != "LOW" else 60),
        "source": source
    }
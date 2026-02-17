# app/services/response_formatter.py

def format_security_response(
    risk: str,
    score: int,
    category: str,
    explanation: str,
    tips: list,
    source: str
):
    return {
        "type": "security",
        "risk": risk,
        "score": score,
        "category": category,
        "explanation": explanation,
        "tips": tips,
        "source": source  # hybrid | url | image | llm
    }

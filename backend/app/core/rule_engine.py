import re

SCAM_RULES = {
    "otp": 30,
    "verify account": 25,
    "urgent": 15,
    "click link": 20,
    "payment": 25,
    "gift": 20,
    "free": 20,
    "bank": 20,
    "password": 30
}

def rule_score(text: str):
    score = 0
    hits = []

    lower = text.lower()

    for key, value in SCAM_RULES.items():
        if key in lower:
            score += value
            hits.append(key)

    return {
        "score": min(score, 100),
        "hits": hits
    }

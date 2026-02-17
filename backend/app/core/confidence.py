# app/core/confidence.py

def normalize_confidence(score: int):
    if score >= 80:
        return 95
    if score >= 60:
        return 80
    if score >= 40:
        return 60
    return 40

import re

PATTERNS = {
    r"\botp\b": 30,
    r"\bverify\b": 25,
    r"\burgent\b": 20,
    r"\bpassword\b": 30,
    r"\bclick\b": 15,
    r"\bprize\b": 20,
}

EDUCATIONAL_CONTEXT = [
    "what is",
    "how does",
    "explain",
    "example of",
    "educational"
]

def rule_score(text: str):

    lower = text.lower()

    if any(ctx in lower for ctx in EDUCATIONAL_CONTEXT):
        return {"score": 0, "hits": []}

    score = 0
    hits = []

    for pattern, weight in PATTERNS.items():
        if re.search(pattern, lower):
            score += weight
            hits.append(pattern)

    return {"score": min(score, 100), "hits": hits}
from transformers import pipeline
import re

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

LABELS = [
    "scam message",
    "phishing link",
    "payment request",
    "malware or app",
    "general security question"
]

def classify_intent(text: str):

    lower = text.lower()

    # ---------- HARD RULES ----------
    if re.search(r"(http://|https://|www\.)", lower):
        return {"intent": "URL", "score": 70}

    if re.search(r"\b[a-f0-9]{64}\b", lower):
        return {"intent": "APP_OR_HASH", "score": 60}

    scam_words = ["congratulations", "winner", "prize", "urgent", "verify"]
    if any(w in lower for w in scam_words):
        return {"intent": "SCAM_TEXT", "score": 75}

    payment_words = ["send money", "transfer", "gift card", "crypto", "pay me"]
    if any(w in lower for w in payment_words):
        return {"intent": "PAYMENT_REQUEST", "score": 80}

    # ---------- ML FALLBACK ----------
    result = classifier(text, LABELS)
    label = result["labels"][0]

    if label == "scam message":
        return {"intent": "SCAM_TEXT", "score": 70}

    if label == "phishing link":
        return {"intent": "URL", "score": 70}

    if label == "payment request":
        return {"intent": "PAYMENT_REQUEST", "score": 75}

    if label == "malware or app":
        return {"intent": "APP_OR_HASH", "score": 65}

    return {"intent": "GENERAL_QUESTION", "score": 10}

# app/services/intent_classifier.py

from transformers import pipeline
import re
import threading

# =====================================================
# MODEL INITIALIZATION (THREAD-SAFE)
# =====================================================

_classifier = None
_model_lock = threading.Lock()

LABELS = [
    "scam message",
    "phishing link",
    "payment request",
    "malware or app",
    "general security question"
]


def get_classifier():
    global _classifier
    if _classifier is None:
        with _model_lock:
            if _classifier is None:
                _classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
    return _classifier


# =====================================================
# INTENT CLASSIFICATION
# =====================================================

def classify_intent(text: str):

    text = text or ""
    lower = text.lower()

    # ---------------------------
    # HARD RULES (FAST PATH)
    # ---------------------------

    if re.search(r"(http://|https://|www\.)", lower):
        return {"intent": "URL", "score": 75}

    if re.search(r"\b[a-f0-9]{64}\b", lower):
        return {"intent": "APP_OR_HASH", "score": 65}

    scam_words = ["congratulations", "winner", "prize", "urgent", "verify", "otp"]
    if any(w in lower for w in scam_words):
        return {"intent": "SCAM_TEXT", "score": 80}

    payment_words = ["send money", "transfer", "gift card", "crypto", "pay me", "upi"]
    if any(w in lower for w in payment_words):
        return {"intent": "PAYMENT_REQUEST", "score": 85}

    # ---------------------------
    # ML FALLBACK
    # ---------------------------

    try:
        classifier = get_classifier()
        result = classifier(text, LABELS)
        label = result["labels"][0]
    except Exception:
        return {"intent": "GENERAL_QUESTION", "score": 20}

    if label == "scam message":
        return {"intent": "SCAM_TEXT", "score": 70}

    if label == "phishing link":
        return {"intent": "URL", "score": 70}

    if label == "payment request":
        return {"intent": "PAYMENT_REQUEST", "score": 75}

    if label == "malware or app":
        return {"intent": "APP_OR_HASH", "score": 65}

    return {"intent": "GENERAL_QUESTION", "score": 15}
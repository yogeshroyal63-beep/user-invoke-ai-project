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

    # Hard rules first
    if re.search(r"(http://|https://|www\.)", lower):
        return "URL"

    if re.search(r"\b[a-f0-9]{64}\b", lower):
        return "APP_OR_HASH"

    scam_words = ["congratulations", "winner", "prize", "urgent", "verify"]
    if any(w in lower for w in scam_words):
        return "SCAM_TEXT"

    payment_words = ["send money", "transfer", "gift card", "crypto", "pay me"]
    if any(w in lower for w in payment_words):
        return "PAYMENT_REQUEST"

    # ML fallback
    result = classifier(text, LABELS)
    label = result["labels"][0]

    if label == "scam message":
        return "SCAM_TEXT"
    if label == "phishing link":
        return "URL"
    if label == "payment request":
        return "PAYMENT_REQUEST"
    if label == "malware or app":
        return "APP_OR_HASH"

    return "GENERAL_QUESTION"

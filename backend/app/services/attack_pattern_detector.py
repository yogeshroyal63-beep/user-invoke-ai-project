# app/services/attack_pattern_detector.py

def detect_attack_pattern(text: str):

    lower = text.lower()

    if any(word in lower for word in ["urgent", "immediately", "act now", "limited time"]):
        return "Urgency Manipulation"

    if any(word in lower for word in ["verify account", "login now", "confirm identity"]):
        return "Credential Phishing"

    if any(word in lower for word in ["winner", "congratulations", "prize", "lottery"]):
        return "Fake Reward Scam"

    if any(word in lower for word in ["send money", "gift card", "crypto", "transfer"]):
        return "Payment Fraud"

    if any(word in lower for word in ["download", "install app", ".apk", ".exe"]):
        return "Malware Distribution"

    return "Unknown Social Engineering Pattern"

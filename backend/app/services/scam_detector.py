def quick_scan(text: str):
    t = text.lower()

    # OTP SCAM
    if "otp" in t or "verification code" in t:
        return {
            "type": "scam",
            "risk": "HIGH",
            "explanation": "OTP requests are commonly used in account takeover scams.",
            "tips": [
                "Never share OTP",
                "Banks never ask OTP by message",
                "Block sender"
            ]
        }

    # MONEY SCAM
    money_words = ["send money", "pay", "transfer", "gift card", "crypto"]
    if any(w in t for w in money_words):
        return {
            "type": "scam",
            "risk": "HIGH",
            "explanation": "Unexpected payment request detected.",
            "tips": [
                "Do not send money",
                "Verify identity",
                "Report scam"
            ]
        }

    # LINKS
    if "http://" in t or "https://" in t or "www." in t or "bit.ly" in t:
        return {
            "type": "scam",
            "risk": "MEDIUM",
            "explanation": "Unknown links may be phishing.",
            "tips": [
                "Do not click",
                "Check domain",
                "Use official site"
            ]
        }

    # NORMAL CHAT FAST PATH
    if len(t.split()) <= 3:
        return {
            "type": "chat",
            "reply": "Hello 👋 How can I help?"
        }

    return None

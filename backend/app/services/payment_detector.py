def analyze_payment(text):

    risky_words = ["gift card", "crypto", "wire", "urgent"]

    hits = sum(1 for w in risky_words if w in text.lower())
    score = min(hits * 0.25, 1.0)

    return {
        "score": score,
        "signals": ["risky_payment_method"]
    }

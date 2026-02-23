import re

# ===============================
# PATTERNS
# ===============================

CRYPTO_PATTERN = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"
ETH_PATTERN = r"\b0x[a-fA-F0-9]{40}\b"
BANK_ACCOUNT_PATTERN = r"\b\d{12,18}\b"
UPI_ID_PATTERN = r"\b[\w.\-]{3,}@[a-zA-Z]{2,}\b"

PAYMENT_CONTEXT_WORDS = [
    "send",
    "transfer",
    "pay",
    "payment",
    "urgent",
    "immediately",
    "now",
    "wire"
]

RISKY_KEYWORDS = [
    "gift card",
    "crypto",
    "bitcoin",
    "otp",
    "verification code"
]


# ===============================
# HELPER
# ===============================

def is_random_upi_id(upi_id: str):
    digits = sum(c.isdigit() for c in upi_id)
    ratio = digits / max(len(upi_id), 1)

    if ratio > 0.5:
        return True

    if re.search(r"[a-z0-9]{8,}", upi_id.lower()):
        return True

    return False


# ===============================
# MAIN FUNCTION
# ===============================

def analyze_payment(text: str):

    lower = text.lower()
    score = 0.0
    signals = []

    # --------------------------------
    # Context keywords
    # --------------------------------

    context_present = any(word in lower for word in PAYMENT_CONTEXT_WORDS)

    for word in RISKY_KEYWORDS:
        if word in lower:
            score += 0.15
            signals.append(f"keyword:{word}")

    # --------------------------------
    # Crypto detection
    # --------------------------------

    if re.search(CRYPTO_PATTERN, text):
        score += 0.5
        signals.append("crypto_wallet_detected")

    if re.search(ETH_PATTERN, text):
        score += 0.5
        signals.append("eth_wallet_detected")

    # --------------------------------
    # Bank account detection
    # --------------------------------

    accounts = re.findall(BANK_ACCOUNT_PATTERN, text)
    if accounts:
        score += 0.4
        signals.append("bank_account_detected")

        if context_present:
            score += 0.2

    # --------------------------------
    # UPI detection (context aware)
    # --------------------------------

    upi_ids = re.findall(UPI_ID_PATTERN, text)

    for upi in upi_ids:
        signals.append(f"upi_id:{upi}")

        # Base detection low weight
        score += 0.1

        if is_random_upi_id(upi):
            score += 0.2
            signals.append("random_upi_id")

        # Escalate ONLY if payment intent exists
        if context_present:
            score += 0.3

    score = min(score, 1.0)

    return {
        "score": score,
        "signals": signals
    }
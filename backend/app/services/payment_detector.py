# app/services/payment_detector.py

import re


RISKY_WORDS = [
    "gift card",
    "crypto",
    "wire transfer",
    "wire",
    "bitcoin",
    "usdt",
    "urgent",
    "immediately",
    "send money",
    "transfer now",
    "otp",
    "verification code"
]

UPI_PATTERN = r"upi://pay\?([^ ]+)"
UPI_ID_PATTERN = r"[\w.\-]{2,}@[a-zA-Z]{2,}"


def extract_upi_params(text: str):
    match = re.search(UPI_PATTERN, text)
    if not match:
        return {}

    params_str = match.group(1)
    params = {}

    for part in params_str.split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            params[k] = v

    return params


def is_random_upi_id(upi_id: str):
    # Numeric-heavy or random-looking IDs
    digits = sum(c.isdigit() for c in upi_id)
    ratio = digits / max(len(upi_id), 1)

    if ratio > 0.5:
        return True

    if re.search(r"[a-z0-9]{10,}", upi_id.lower()):
        return True

    return False


def analyze_payment(text: str):

    lower = text.lower()
    score = 0.0
    signals = []

    # ---------------------------
    # Keyword-based detection
    # ---------------------------
    for word in RISKY_WORDS:
        if word in lower:
            score += 0.1
            signals.append(f"keyword:{word}")

    # ---------------------------
    # UPI Link Detection
    # ---------------------------
    upi_params = extract_upi_params(text)

    if upi_params:
        score += 0.3
        signals.append("upi_link_detected")

        pa = upi_params.get("pa")
        pn = upi_params.get("pn")

        if pa:
            signals.append(f"upi_id:{pa}")

            if is_random_upi_id(pa):
                score += 0.2
                signals.append("random_upi_id")

        if not pn:
            score += 0.1
            signals.append("missing_payee_name")

    # ---------------------------
    # Direct UPI ID detection
    # ---------------------------
    direct_upi = re.findall(UPI_ID_PATTERN, text)

    for upi in direct_upi:
        score += 0.2
        signals.append(f"upi_id_detected:{upi}")

        if is_random_upi_id(upi):
            score += 0.2
            signals.append("random_upi_id")

    score = min(score, 1.0)

    return {
        "score": score,
        "signals": signals
    }
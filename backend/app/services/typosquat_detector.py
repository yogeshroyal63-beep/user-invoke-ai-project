# app/services/typosquat_detector.py

from difflib import SequenceMatcher

POPULAR_DOMAINS = [
    "google.com",
    "facebook.com",
    "amazon.com",
    "microsoft.com",
    "apple.com",
    "paypal.com",
    "instagram.com",
    "linkedin.com"
]

def is_typosquatted(domain: str):

    for legit in POPULAR_DOMAINS:
        ratio = SequenceMatcher(None, domain, legit).ratio()
        if 0.75 < ratio < 1.0:
            return True, legit

    return False, None

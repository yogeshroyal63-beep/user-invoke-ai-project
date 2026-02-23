import re

BRANDS = [
    "paypal",
    "google",
    "amazon",
    "bank",
    "instagram",
    "facebook",
    "microsoft"
]


def detect_brand_impersonation(url: str):

    domain = url.lower()

    flags = []

    for brand in BRANDS:
        if brand in domain and not domain.startswith(brand):
            flags.append(f"{brand}_impersonation")

    return flags
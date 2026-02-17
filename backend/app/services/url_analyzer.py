# app/services/url_analyzer.py

import tldextract
import requests
import time
from difflib import SequenceMatcher

TRUSTED_DOMAINS = [
    "chatgpt.com",
    "openai.com",
    "google.com",
    "github.com",
    "stackoverflow.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "linkedin.com",
    "youtube.com"
]

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

VIRUSTOTAL_API_KEY = ""  # optional


# --------------------------
# Helpers
# --------------------------

def domain_age_days(domain):
    try:
        url = f"https://api.whois.vu/?q={domain}"
        r = requests.get(url, timeout=5)
        data = r.json()
        created = data.get("created")
        if not created:
            return None
        created_ts = time.mktime(time.strptime(created, "%Y-%m-%d"))
        return (time.time() - created_ts) / 86400
    except:
        return None


def is_typosquatted(domain: str):
    for legit in POPULAR_DOMAINS:
        ratio = SequenceMatcher(None, domain, legit).ratio()
        if 0.75 < ratio < 1.0:
            return True, legit
    return False, None


# --------------------------
# Main Analyzer
# --------------------------

def analyze_url(url: str):

    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"

    # Whitelist check
    if domain in TRUSTED_DOMAINS:
        return {
            "score": 0,
            "signals": ["trusted_domain"],
            "risk": "LOW",
            "explanation": "This is a well-known trusted website.",
            "tips": ["No action needed"]
        }

    score = 0.0
    signals = []
    explanation = "The link shows characteristics commonly used in phishing attacks."

    # Hyphen trick
    if "-" in ext.domain:
        score += 0.25
        signals.append("hyphen_domain")

    # URL shorteners
    if domain in ["bit.ly", "tinyurl.com", "t.co"]:
        score += 0.4
        signals.append("url_shortener")

    # Domain age
    age = domain_age_days(domain)
    if age is not None and age < 30:
        score += 0.4
        signals.append("new_domain")

    # Typosquatting
    typo_flag, legit_domain = is_typosquatted(domain)
    if typo_flag:
        score += 0.5
        signals.append("possible_typosquatting")
        explanation = f"This domain looks similar to {legit_domain}, which may indicate a phishing attempt."

    # VirusTotal check (optional)
    if VIRUSTOTAL_API_KEY:
        try:
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}
            r = requests.get(
                f"https://www.virustotal.com/api/v3/domains/{domain}",
                headers=headers,
                timeout=5
            )
            if r.status_code == 200:
                stats = r.json()["data"]["attributes"]["last_analysis_stats"]
                if stats.get("malicious", 0) > 0:
                    score += 0.7
                    signals.append("virustotal_malicious")
        except:
            pass

    # Normalize score (0–1 scale)
    score = min(score, 1.0)

    # Risk levels
    if score >= 0.7:
        risk = "HIGH"
    elif score >= 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "score": round(score * 100),
        "signals": signals,
        "risk": risk,
        "explanation": explanation,
        "tips": [
            "Do not click the link if unsure",
            "Verify the sender identity",
            "Check the domain spelling carefully",
            "Report suspicious links"
        ]
    }

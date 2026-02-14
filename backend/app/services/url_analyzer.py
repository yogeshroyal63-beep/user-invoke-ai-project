import tldextract
import requests
import time

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

VIRUSTOTAL_API_KEY = ""   # optional


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


def analyze_url(url):

    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"

    # ✅ WHITELIST CHECK
    if domain in TRUSTED_DOMAINS:
        return {
            "score": 0.0,
            "signals": ["trusted_domain"],
            "risk": "LOW",
            "explanation": "This is a well-known trusted website.",
            "tips": ["No action needed"]
        }

    score = 0.0
    signals = []

    # Hyphen trick
    if "-" in ext.domain:
        score += 0.25
        signals.append("hyphen_domain")

    # Shorteners
    if domain in ["bit.ly", "tinyurl.com", "t.co"]:
        score += 0.4
        signals.append("url_shortener")

    # Domain age
    age = domain_age_days(domain)
    if age is not None and age < 30:
        score += 0.4
        signals.append("new_domain")

    # VirusTotal (optional)
    if VIRUSTOTAL_API_KEY:
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        r = requests.get(
            f"https://www.virustotal.com/api/v3/domains/{domain}",
            headers=headers
        )
        if r.status_code == 200:
            stats = r.json()["data"]["attributes"]["last_analysis_stats"]
            if stats["malicious"] > 0:
                score += 0.7
                signals.append("virustotal_malicious")

    # Normalize
    score = min(score, 1.0)

    if score >= 0.7:
        risk = "HIGH"
    elif score >= 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "score": score,
        "signals": signals,
        "risk": risk,
        "explanation": "The link shows characteristics commonly used in phishing attacks.",
        "tips": [
            "Do not click the link",
            "Verify sender identity",
            "Check domain spelling",
            "Report the link"
        ]
    }

import requests
import tldextract
import time

VIRUSTOTAL_API_KEY = ""  # optional

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

    score = 0.0
    signals = []

    # Hyphen trick
    if "-" in ext.domain:
        score += 0.3
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

    return {
        "score": min(score, 1.0),
        "signals": signals
    }

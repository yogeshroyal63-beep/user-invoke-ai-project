import requests
import tldextract
import time
import socket
import ssl
import hashlib

VT_API_KEY = ""   # optional
GSB_API_KEY = ""  # optional

# --------------------------
# Helpers
# --------------------------

def domain_age(domain):
    try:
        r = requests.get(f"https://api.whois.vu/?q={domain}", timeout=6)
        data = r.json()
        created = data.get("created")
        if not created:
            return None
        ts = time.mktime(time.strptime(created, "%Y-%m-%d"))
        return (time.time() - ts) / 86400
    except:
        return None


def has_https(url):
    return url.startswith("https://")


def check_tls(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            return True
    except:
        return False


def is_ip_url(domain):
    parts = domain.split(".")
    return all(p.isdigit() for p in parts)


def suspicious_tld(tld):
    bad = ["zip", "mov", "tk", "xyz", "top"]
    return tld in bad


# --------------------------
# Reputation APIs
# --------------------------

def virustotal(domain):
    if not VT_API_KEY:
        return 0
    h = {"x-apikey": VT_API_KEY}
    r = requests.get(
        f"https://www.virustotal.com/api/v3/domains/{domain}",
        headers=h
    )
    if r.status_code != 200:
        return 0
    stats = r.json()["data"]["attributes"]["last_analysis_stats"]
    return stats.get("malicious", 0)


def google_safe_browsing(url):
    if not GSB_API_KEY:
        return False
    body = {
        "client": {"clientId": "trustcheck", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    r = requests.post(
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GSB_API_KEY}",
        json=body
    )
    return bool(r.json().get("matches"))


# --------------------------
# MAIN ENGINE
# --------------------------

def scan_url(url: str):

    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"

    score = 100
    signals = []

    # HTTPS
    if not has_https(url):
        score -= 15
        signals.append("no_https")

    # TLS
    if not check_tls(domain):
        score -= 10
        signals.append("bad_tls")

    # Domain age
    age = domain_age(domain)
    if age and age < 30:
        score -= 20
        signals.append("new_domain")

    # IP URL
    if is_ip_url(ext.domain):
        score -= 25
        signals.append("ip_url")

    # Hyphen trick
    if "-" in ext.domain:
        score -= 10
        signals.append("hyphen_domain")

    # Suspicious TLD
    if suspicious_tld(ext.suffix):
        score -= 15
        signals.append("bad_tld")

    # VirusTotal
    if virustotal(domain) > 0:
        score -= 40
        signals.append("virustotal_flag")

    # Google Safe Browsing
    if google_safe_browsing(url):
        score -= 40
        signals.append("google_flag")

    score = max(score, 0)

    if score >= 75:
        verdict = "SAFE"
    elif score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "HIGH_RISK"

    return {
        "url": url,
        "score": score,
        "verdict": verdict,
        "signals": signals
    }

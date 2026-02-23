# app/services/url_trust_engine.py

import re
import whois
import socket
import ssl
import math
from urllib.parse import urlparse
from datetime import datetime


def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if creation:
            return (datetime.now() - creation).days
    except:
        pass
    return None


def check_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            return True
    except:
        return False


def reverse_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        host = socket.gethostbyaddr(ip)
        return host[0]
    except:
        return None


def calculate_entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob])


def scan_url(url):

    score = 0
    signals = []

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if url.startswith("http://"):
        score += 20
        signals.append("no_https")

    if re.search(r"\d+\.\d+\.\d+\.\d+", domain):
        score += 40
        signals.append("ip_address_link")

    suspicious_tlds = [".xyz", ".tk", ".ru", ".cn", ".top"]
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        score += 30
        signals.append("suspicious_tld")

    age = get_domain_age(domain)
    if age is not None and age < 30:
        score += 40
        signals.append("new_domain")

    if not check_ssl(domain):
        score += 20
        signals.append("invalid_ssl")

    rdns = reverse_dns(domain)
    if rdns and domain not in rdns:
        score += 20
        signals.append("reverse_dns_mismatch")

    if calculate_entropy(domain) > 4:
        score += 25
        signals.append("high_entropy")

    if score >= 90:
        verdict = "HIGH_RISK"
    elif score >= 50:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return {
        "verdict": verdict,
        "score": score,
        "signals": signals
    }
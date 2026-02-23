import socket
import whois
from datetime import datetime


def reverse_dns_lookup(domain: str):
    try:
        return socket.gethostbyname(domain)
    except:
        return None


def domain_age_check(domain: str):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            return None

        age_days = (datetime.utcnow() - creation_date).days
        return age_days
    except:
        return None


def analyze_domain_intelligence(domain: str):

    ip = reverse_dns_lookup(domain)
    age_days = domain_age_check(domain)

    signals = {
        "ip_resolved": bool(ip),
        "domain_age_days": age_days,
        "new_domain": age_days is not None and age_days < 90
    }

    score = 0

    if not ip:
        score += 40

    if age_days is not None and age_days < 30:
        score += 50
    elif age_days is not None and age_days < 90:
        score += 30

    return signals, score
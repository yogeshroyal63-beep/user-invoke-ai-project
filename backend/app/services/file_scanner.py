# app/services/file_scanner.py

import hashlib
import re
import os
import requests

SUSPICIOUS_EXTENSIONS = [
    ".exe", ".apk", ".bat", ".cmd", ".scr",
    ".js", ".vbs", ".jar", ".msi", ".ps1"
]

DOUBLE_EXTENSION_PATTERN = r"\.(jpg|png|pdf|doc|docx)\.(exe|js|bat|scr|cmd)$"

VIRUSTOTAL_API_KEY = os.getenv("VT_API_KEY", "")


def calculate_hash(content: bytes):
    return hashlib.sha256(content).hexdigest()


def scan_virustotal_hash(file_hash: str):
    if not VIRUSTOTAL_API_KEY:
        return 0

    try:
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        r = requests.get(url, headers=headers, timeout=8)

        if r.status_code != 200:
            return 0

        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        return stats.get("malicious", 0)
    except:
        return 0


def scan_file(filename: str, content: bytes):

    score = 0
    signals = []

    lower = filename.lower()

    # 1️⃣ Extension check
    for ext in SUSPICIOUS_EXTENSIONS:
        if lower.endswith(ext):
            score += 60
            signals.append("suspicious_extension")
            break

    # 2️⃣ Double extension trick
    if re.search(DOUBLE_EXTENSION_PATTERN, lower):
        score += 30
        signals.append("double_extension_attack")

    # 3️⃣ Generate hash
    file_hash = calculate_hash(content)

    # 4️⃣ VirusTotal check
    vt_hits = scan_virustotal_hash(file_hash)
    if vt_hits > 0:
        score += 50
        signals.append("virustotal_malicious")

    score = min(score, 100)

    # 5️⃣ Risk classification
    if score >= 75:
        risk = "HIGH"
    elif score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "type": "file",
        "filename": filename,
        "risk": risk,
        "score": score,
        "signals": signals,
        "hash": file_hash,
        "explanation": (
            "This file shows characteristics commonly used in malware distribution."
            if score > 0 else
            "No strong malicious indicators detected."
        ),
        "tips": [
            "Do not open unknown attachments.",
            "Verify sender identity.",
            "Scan file with antivirus software."
        ] if score > 0 else [
            "File appears safe but remain cautious."
        ]
    }
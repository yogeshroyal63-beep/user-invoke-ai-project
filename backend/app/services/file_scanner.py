# app/services/file_scanner.py

import hashlib

SUSPICIOUS_EXTENSIONS = [
    ".exe", ".apk", ".bat", ".cmd", ".scr", ".js", ".vbs", ".jar"
]

def scan_file(filename: str, content: bytes):

    score = 0
    signals = []

    lower = filename.lower()

    # Extension check
    for ext in SUSPICIOUS_EXTENSIONS:
        if lower.endswith(ext):
            score += 70
            signals.append("suspicious_extension")
            break

    # Double extension trick
    if "." in lower and lower.count(".") > 1:
        score += 20
        signals.append("double_extension")

    # Hash generation (future blacklist integration)
    file_hash = hashlib.sha256(content).hexdigest()

    if score >= 70:
        risk = "HIGH"
    elif score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "type": "file",
        "filename": filename,
        "risk": risk,
        "score": min(score, 100),
        "signals": signals,
        "hash": file_hash,
        "explanation": "This file shows characteristics commonly used in malware distribution." if score else "No strong malicious indicators detected.",
        "tips": [
            "Do not open unknown attachments",
            "Verify sender identity",
            "Scan file with antivirus software"
        ] if score else ["File appears safe but remain cautious."]
    }

import requests

VIRUSTOTAL_API_KEY = ""  # optional

def analyze_app(text):

    score = 0.0
    signals = []

    # Hash detection
    if len(text) == 64:
        signals.append("sha256_hash")

        if VIRUSTOTAL_API_KEY:
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}
            r = requests.get(
                f"https://www.virustotal.com/api/v3/files/{text}",
                headers=headers
            )
            if r.status_code == 200:
                stats = r.json()["data"]["attributes"]["last_analysis_stats"]
                if stats["malicious"] > 0:
                    score = 0.9
                    signals.append("virustotal_malware")
                else:
                    score = 0.2
            else:
                score = 0.4
        else:
            score = 0.4

    # App name
    else:
        signals.append("unknown_app")
        score = 0.5

    return {
        "score": score,
        "signals": signals
    }

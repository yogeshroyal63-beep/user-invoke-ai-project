import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_with_ollama(message: str):

    prompt = f"""
You are TrustCheck AI cybersecurity assistant.

Return ONLY valid JSON.

If scam:

{{
  "type": "scam",
  "category": "Phishing | OTP Scam | Fake Prize | Malware | Payment Fraud",
  "risk": "HIGH | MEDIUM | LOW",
  "confidence": 0-100,
  "explanation": "Detailed explanation",
  "tips": ["tip1","tip2","tip3"]
}}

If normal chat:

{{
  "type": "chat",
  "reply": "Friendly reply"
}}

Message:
{message}
"""

    res = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )

    raw = res.json().get("response", "")

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        clean = raw[start:end]
        parsed = json.loads(clean)

        if parsed.get("type") == "chat":
            return {
                "type": "chat",
                "reply": parsed.get("reply", "Hello 👋")
            }

        if parsed.get("type") == "scam":
            return {
                "type": "scam",
                "category": parsed.get("category", "Scam"),
                "risk": parsed.get("risk", "HIGH"),
                "confidence": parsed.get("confidence", 90),
                "explanation": parsed.get("explanation", ""),
                "tips": parsed.get("tips", [])
            }

    except:
        pass

    return {
        "type": "chat",
        "reply": "Hello 👋 How can I help?"
    }

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_with_ollama(message: str):
    prompt = f"""
You are TrustCheck AI.

If the message is a scam or phishing attempt,
return JSON in this format:

{{
  "type": "scam",
  "risk": "HIGH or MEDIUM or LOW",
  "explanation": "Explain clearly",
  "tips": ["tip1", "tip2", "tip3"]
}}

If the message is normal conversation,
return JSON in this format:

{{
  "type": "chat",
  "reply": "friendly helpful response"
}}

Message:
{message}
"""

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = res.json()

    # ✅ OLLAMA sometimes returns "response" OR "message"
    raw = data.get("response") or data.get("message") or ""

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "type": "chat",
            "reply": raw if raw else "Hello! How can I help you?"
        }

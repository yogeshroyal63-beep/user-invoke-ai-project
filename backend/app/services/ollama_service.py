import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_with_ollama(message: str):
    prompt = f"""
You are TrustCheck AI.

If the message is scam or phishing, return JSON:

{{
  "type": "scam",
  "risk": "HIGH",
  "explanation": "Explain why",
  "tips": ["tip1", "tip2"]
}}

If normal conversation, return JSON:

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

    raw = res.json()["response"]

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "type": "chat",
            "reply": raw
        }

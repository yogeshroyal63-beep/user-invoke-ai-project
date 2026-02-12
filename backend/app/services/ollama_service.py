import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_with_ollama(message: str):
    prompt = f"""
You are a cybersecurity assistant.

Analyze the following message and return STRICT JSON in this format:

{{
  "risk": "LOW RISK | MEDIUM RISK | HIGH RISK",
  "explanation": "short explanation",
  "tips": ["tip1", "tip2", "tip3"]
}}

Message:
{message}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=120)
        res.raise_for_status()

        raw = res.json()["response"]

        # Extract JSON from model output
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_text = raw[start:end]

        return json.loads(json_text)

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return {
            "risk": "UNKNOWN",
            "explanation": "AI response could not be parsed.",
            "tips": []
        }

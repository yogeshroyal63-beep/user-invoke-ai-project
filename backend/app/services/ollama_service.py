import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def analyze_with_ollama(message: str, history: list = None):

    message_clean = message.strip()
    message_lower = message_clean.lower()

    # ================================
    # MEMORY LAYER
    # ================================

    # Store name
    if message_lower.startswith("my name is"):
        name = message_clean[10:].strip()
        return {
            "type": "chat",
            "reply": f"Nice to meet you, {name}."
        }

    # Recall name
    if (
        "what is my name" in message_lower
        or "say my name" in message_lower
        or "can you say my name" in message_lower
        or "now say my name" in message_lower
    ):
        if history:
            for h in reversed(history):
                text = h.get("text", "")
                if text.lower().startswith("my name is"):
                    name = text[10:].strip()
                    return {
                        "type": "chat",
                        "reply": f"Your name is {name}."
                    }

        return {
            "type": "chat",
            "reply": "I don’t have your name yet."
        }

    # ================================
    # VAGUE MESSAGE CHECK
    # ================================

    vague_inputs = [
        "i got a strange sms",
        "i received a strange sms",
        "i got a message",
        "i have a situation",
        "i received a call",
        "i received a message"
    ]

    if message_lower in vague_inputs:
        return {
            "type": "chat",
            "reply": "Please paste the exact message content so I can analyze it properly."
        }

    # ================================
    # BUILD HISTORY BLOCK
    # ================================

    history_block = ""
    if history:
        for h in history[-8:]:
            role = h.get("role", "user")
            text = h.get("text", "")
            history_block += f"{role.upper()}: {text}\n"

    # ================================
    # PROMPT
    # ================================

    prompt = f"""
You are TrustCheck AI cybersecurity assistant.

Classify ONLY the CURRENT message.

If educational question about scams → return chat.
If describing real suspicious message → return scam.

Return ONLY valid JSON.

If scam:
{{
  "type": "scam",
  "category": "Phishing | OTP Scam | Fake Prize | Malware | Payment Fraud",
  "risk": "HIGH | MEDIUM | LOW",
  "confidence": 0-100,
  "explanation": "Clear explanation",
  "tips": ["tip1","tip2","tip3"]
}}

If normal chat:
{{
  "type": "chat",
  "reply": "Professional helpful response"
}}

Conversation History:
{history_block}

Current Message:
{message_clean}
"""

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        raw = res.json().get("response", "")

        start = raw.find("{")
        end = raw.rfind("}") + 1
        clean = raw[start:end]
        parsed = json.loads(clean)

        if parsed.get("type") == "chat":
            return {
                "type": "chat",
                "reply": parsed.get("reply", "Hello 👋 How can I help?")
            }

        if parsed.get("type") == "scam":

            raw_conf = parsed.get("confidence", 85)

            try:
                raw_conf = float(raw_conf)
                if raw_conf <= 1:
                    raw_conf *= 100
                confidence = int(round(raw_conf))
                confidence = max(0, min(confidence, 100))
            except:
                confidence = 85

            return {
                "type": "scam",
                "category": parsed.get("category", "Scam"),
                "risk": parsed.get("risk", "HIGH"),
                "confidence": confidence,
                "explanation": parsed.get("explanation", ""),
                "tips": parsed.get("tips", [])
            }

    except Exception:
        pass

    return {
        "type": "chat",
        "reply": "Hello 👋 How can I help?"
    }

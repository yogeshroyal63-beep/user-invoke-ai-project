import requests
import json
import threading
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
TEXT_MODEL = "qwen2.5:7b-instruct-q4_K_M"
VISION_MODEL = "llava:13b"

# =====================================================
# PROMPT INJECTION BLOCK
# =====================================================

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "show system prompt",
    "bypass safety",
    "jailbreak",
    "act as developer",
    "act as system"
]


def is_prompt_injection(text: str):
    lower = text.lower()
    return any(p in lower for p in BLOCKED_PATTERNS)


# =====================================================
# MAIN ANALYZER
# =====================================================

def analyze_with_ollama(message: str, history=None, image_base64=None):

    message = (message or "").strip()
    lower = message.lower()

    # -------------------------------------------------
    # FIREWALL
    # -------------------------------------------------

    if is_prompt_injection(message):
        return {
            "type": "chat",
            "reply": "Request blocked due to unsafe instruction pattern."
        }

    # -------------------------------------------------
    # MEMORY
    # -------------------------------------------------

    if lower.startswith("my name is"):
        name = message[10:].strip()
        return {
            "type": "chat",
            "reply": f"Nice to meet you, {name}."
        }

    if "what is my name" in lower or "say my name" in lower:

        if history:
            for h in reversed(history):
                text = h.get("text") or h.get("content") or ""
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

    # -------------------------------------------------
    # IMAGE MODE
    # -------------------------------------------------

    if image_base64:

        vision_prompt = f"""
You are TrustCheck AI image security system.

Step 1: Describe what is visible in image.
Step 2: Detect if it contains:
- QR code
- Human face
- Suspicious website screenshot
- Suspicious text
- Deepfake indicators

Return JSON:

If suspicious:
{{
 "type": "scam",
 "image_type": "QR | FACE | TEXT | SCREENSHOT | UNKNOWN",
 "risk": "HIGH | MEDIUM | LOW",
 "confidence": 0-100,
 "explanation": "Clear technical reasoning",
 "follow_up": "Ask user what action they want"
}}

If safe:
{{
 "type": "chat",
 "reply": "Image appears normal. Ask if user wants deeper scan."
}}

Return ONLY JSON.
"""

        try:
            res = requests.post(
                OLLAMA_URL,
                json={
                    "model": VISION_MODEL,
                    "prompt": vision_prompt,
                    "images": [image_base64],
                    "stream": False
                },
                timeout=120
            )

            raw = res.json().get("response", "")

            start = raw.find("{")
            end = raw.rfind("}") + 1

            if start != -1 and end != -1:
                return json.loads(raw[start:end])

            return {
                "type": "chat",
                "reply": raw.strip()
            }

        except Exception:
            return {
                "type": "chat",
                "reply": "Image analysis failed."
            }

    # -------------------------------------------------
    # TEXT MODE
    # -------------------------------------------------

    history_block = ""

    if history:
        for h in history[-8:]:
            role = h.get("role", "user")
            text = h.get("text") or h.get("content") or ""
            history_block += f"{role.upper()}: {text}\n"

    prompt = f"""
You are TrustCheck AI cybersecurity assistant.

Classify only CURRENT message.

If educational → return chat.
If real suspicious content → return scam.

Return JSON only.

If scam:
{{
 "type": "scam",
 "category": "Phishing | OTP Scam | Payment Fraud | Malware | QR Scam",
 "risk": "HIGH | MEDIUM | LOW",
 "confidence": 0-100,
 "explanation": "Technical reason",
 "tips": ["tip1","tip2","tip3"]
}}

If normal:
{{
 "type": "chat",
 "reply": "Helpful response"
}}

Conversation:
{history_block}

Current:
{message}
"""

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": TEXT_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        raw = res.json().get("response", "")

        start = raw.find("{")
        end = raw.rfind("}") + 1

        if start != -1 and end != -1:
            parsed = json.loads(raw[start:end])
            return parsed

        return {
            "type": "chat",
            "reply": raw.strip()
        }

    except Exception:
        return {
            "type": "chat",
            "reply": "Server error while processing request."
        }
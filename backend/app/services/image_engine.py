import requests
import json
from PIL import Image
from io import BytesIO

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

async def analyze_image(image, user_text: str):

    image_exists = False

    if image:
        data = await image.read()
        Image.open(BytesIO(data))  # validate image
        image_exists = True

    prompt = f"""
You are TrustCheck AI Vision Security Assistant.

FIRST decide intent:

If user is asking about:
- malware
- phishing
- scam
- QR
- suspicious content

THEN perform security analysis.

If user is asking general question about image → answer normally.

If only image uploaded and no instruction → ask what user wants.

Return ONLY JSON.

--- SECURITY RESPONSE ---
{{
 "type":"scam",
 "risk":"HIGH|MEDIUM|LOW",
 "category":"Malware|Phishing|QR Scam|Deepfake|Suspicious",
 "confidence":0-100,
 "explanation":"plain english",
 "tips":["tip1","tip2"]
}}

--- NORMAL RESPONSE ---
{{
 "type":"chat",
 "reply":"answer"
}}

--- ASK USER ---
{{
 "type":"chat",
 "reply":"What do you want me to do with this image?"
}}

Image Uploaded: {image_exists}
User Instruction: {user_text}
"""

    res = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )

    raw = res.json().get("response","")

    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])

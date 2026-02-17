from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.ollama_service import analyze_with_ollama

router = APIRouter(prefix="/api")


class HistoryItem(BaseModel):
    role: str
    text: str


class ScanRequest(BaseModel):
    message: str
    email: Optional[str] = None
    history: Optional[List[HistoryItem]] = []


@router.post("/scan")
async def unified_scan(req: ScanRequest):

    message = req.message.strip()

    # ✅ Convert history models to dict
    history = []
    if req.history:
        history = [h.dict() for h in req.history]

    # ✅ Pass history to Ollama
    ai_result = analyze_with_ollama(message, history)

    # 1️⃣ Normal conversation
    if ai_result.get("type") == "chat":
        return {
            "type": "chat",
            "reply": ai_result.get("reply", "How can I help?")
        }

    # 2️⃣ Scam result
    if ai_result.get("type") == "scam":
        return {
            "type": "scam",
            "category": ai_result.get("category", "Scam"),
            "risk": ai_result.get("risk", "HIGH"),
            "confidence": ai_result.get("confidence", 90),
            "explanation": ai_result.get("explanation", ""),
            "tips": ai_result.get("tips", [])
        }

    # 3️⃣ Safe fallback
    return {
        "type": "chat",
        "reply": "How can I assist you?"
    }

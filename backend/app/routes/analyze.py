from fastapi import APIRouter
from pydantic import BaseModel
from app.core.risk_engine import calculate_final_risk
from app.services.ollama_service import analyze_with_ollama
from app.services.attack_pattern_detector import detect_attack_pattern

router = APIRouter(prefix="/api")   # ✅ THIS WAS MISSING


class AnalyzeRequest(BaseModel):
    message: str
    email: str | None = None


@router.post("/analyze")
def analyze(req: AnalyzeRequest):

    hybrid = calculate_final_risk(req.message)
    llm = analyze_with_ollama(req.message)

    if llm.get("type") == "chat":
        return llm

    pattern = detect_attack_pattern(req.message)

    return {
        "type": "security",
        "risk": hybrid["risk"],
        "score": hybrid["score"],
        "category": llm.get("category", "Scam"),
        "attack_pattern": pattern,
        "explanation": llm.get("explanation", hybrid.get("explanation")),
        "tips": llm.get("tips", hybrid.get("tips", []))
    }

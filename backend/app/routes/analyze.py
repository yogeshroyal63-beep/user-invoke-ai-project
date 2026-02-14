from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ollama_service import analyze_with_ollama

router = APIRouter(prefix="/api")

class AnalyzeRequest(BaseModel):
    message: str
    email: str | None = None   # make email optional

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    result = analyze_with_ollama(req.message)
    return result

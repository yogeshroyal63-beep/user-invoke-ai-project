from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ollama_service import analyze_with_ollama

router = APIRouter(prefix="/api", tags=["Analysis"])

class AnalyzeRequest(BaseModel):
    message: str

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    return analyze_with_ollama(req.message)

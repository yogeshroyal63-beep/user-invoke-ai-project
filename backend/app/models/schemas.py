from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    content: str

class AnalyzeResponse(BaseModel):
    input_type: str
    risk_level: str
    risk_score: float
    explanation: str
    advice: list[str]

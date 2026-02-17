from app.core.rule_engine import rule_score
from app.services.intent_classifier import classify_intent
from app.services.url_analyzer import analyze_url
from app.services.ollama_service import analyze_with_ollama

def calculate_final_risk(message: str):

    rule = rule_score(message)
    intent = classify_intent(message)
    url = analyze_url(message)
    llm = analyze_with_ollama(message)

    llm_score = llm.get("confidence", 50)

    final_score = int(
        rule["score"] * 0.30 +
        intent["score"] * 0.25 +
        url["score"] * 0.20 +
        llm_score * 0.25
    )

    if final_score >= 70:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "type": "security",
        "risk": level,
        "score": final_score,
        "explanation": llm.get("explanation", ""),
        "tips": llm.get("tips", [])
    }

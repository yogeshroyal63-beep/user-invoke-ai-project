# app/core/risk_engine.py

from app.core.rule_engine import rule_score
from app.services.intent_classifier import classify_intent
from app.services.url_analyzer import analyze_url
from app.services.url_trust_engine import scan_url as deep_url_scan
from app.services.payment_detector import analyze_payment
from app.services.ollama_service import analyze_with_ollama
from app.core.confidence import normalize_confidence
import re


def calculate_final_risk(message: str):

    message = message or ""

    # =====================================================
    # 1️⃣ RULE ENGINE
    # =====================================================
    rule = rule_score(message)
    rule_score_value = rule.get("score", 0)

    # =====================================================
    # 2️⃣ INTENT CLASSIFIER
    # =====================================================
    intent = classify_intent(message)
    intent_score = intent.get("score", 0)

    # =====================================================
    # 3️⃣ URL ANALYSIS (BASIC + DEEP IF PRESENT)
    # =====================================================
    url_score_value = 0
    url_signals = []
    url_risk_level = "LOW"

    if re.search(r"(http://|https://|www\.)", message.lower()):
        basic_url = analyze_url(message)
        deep_url = deep_url_scan(message)

        # Normalize deep_url score (0–100 safe score → convert to risk score)
        deep_risk_score = 100 - deep_url.get("score", 100)

        url_score_value = int((basic_url.get("score", 0) * 0.4) + (deep_risk_score * 0.6))
        url_signals = deep_url.get("signals", [])
        url_risk_level = (
            "HIGH"
            if deep_url.get("verdict") == "HIGH_RISK"
            else "MEDIUM"
            if deep_url.get("verdict") == "SUSPICIOUS"
            else "LOW"
        )

    # =====================================================
    # 4️⃣ PAYMENT ANALYSIS
    # =====================================================
    payment = analyze_payment(message)
    payment_score = int(payment.get("score", 0) * 100)

    # =====================================================
    # 5️⃣ LLM SECURITY LAYER
    # =====================================================
    llm = analyze_with_ollama(message)
    llm_confidence = llm.get("confidence", 50)
    llm_explanation = llm.get("explanation", "")
    llm_tips = llm.get("tips", [])

    # =====================================================
    # 6️⃣ FINAL WEIGHTED SCORING
    # =====================================================
    final_score = int(
        rule_score_value * 0.25 +
        intent_score * 0.20 +
        url_score_value * 0.25 +
        payment_score * 0.10 +
        llm_confidence * 0.20
    )

    final_score = max(0, min(final_score, 100))

    # =====================================================
    # 7️⃣ RISK LEVEL
    # =====================================================
    if final_score >= 75:
        level = "HIGH"
    elif final_score >= 45:
        level = "MEDIUM"
    else:
        level = "LOW"

    # =====================================================
    # 8️⃣ CONFIDENCE NORMALIZATION
    # =====================================================
    normalized_conf = normalize_confidence(final_score)

    # =====================================================
    # 9️⃣ STRUCTURED RESPONSE
    # =====================================================
    return {
        "type": "scam" if level in ["HIGH", "MEDIUM"] else "chat",
        "risk": level,
        "score": final_score,
        "confidence": normalized_conf,
        "category": intent.get("intent", "Security Analysis"),
        "signals": {
            "rule_hits": rule.get("hits", []),
            "url_signals": url_signals,
            "payment_flags": payment.get("signals", [])
        },
        "explanation": llm_explanation if llm_explanation else "Security risk evaluated using multi-layer analysis.",
        "tips": llm_tips if llm_tips else [
            "Verify sender identity.",
            "Avoid urgent payment requests.",
            "Do not click unknown links."
        ]
    }
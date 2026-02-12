from transformers import pipeline

scam_model = pipeline(
    "text-classification",
    model="mrm8488/bert-tiny-finetuned-sms-spam-detection"
)

def analyze_scam(text):

    result = scam_model(text)[0]

    score = result["score"] if result["label"] == "LABEL_1" else 1 - result["score"]

    return {
        "score": round(score, 2),
        "signals": ["ml_spam_model"]
    }

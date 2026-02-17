# app/services/action_intent_detector.py

def detect_action_intent(text: str):

    lower = text.lower()

    mail_keywords = [
        "check my mail",
        "scan my mail",
        "check my emails",
        "scan my inbox",
        "trash dangerous mail",
        "delete dangerous emails"
    ]

    for phrase in mail_keywords:
        if phrase in lower:
            return {
                "type": "action",
                "action": "email_scan"
            }

    return None

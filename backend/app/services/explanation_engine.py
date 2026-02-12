def generate_explanation(intent, risk, result):

    level = risk["level"]

    if intent == "SCAM_TEXT":
        explanation = (
            "This message shows patterns commonly used in scams such as fake rewards, urgency, "
            "or pressure tactics to trick users into acting quickly."
        )

        advice = [
            "Do not reply to the sender",
            "Do not click any links",
            "Block and report the account",
            "Never share OTP, passwords, or payment details"
        ]

    elif intent == "URL":
        explanation = (
            "This link has characteristics often associated with phishing or malicious websites."
        )

        advice = [
            "Do not open the link",
            "Avoid entering any information",
            "Delete the message",
            "Use a trusted website directly instead"
        ]

    elif intent == "PAYMENT_REQUEST":
        explanation = (
            "Requests for urgent or unusual payments are a common scam technique."
        )

        advice = [
            "Do not send money",
            "Verify the requester using another method",
            "Contact your bank if money was sent"
        ]

    elif intent == "APP_OR_HASH":
        explanation = (
            "This file or app cannot be verified as safe and may contain malicious code."
        )

        advice = [
            "Do not install the app",
            "Delete the file",
            "Use only official app stores"
        ]

    else:
        explanation = (
            "No strong malicious indicators were detected, but caution is still recommended."
        )

        advice = [
            "Be careful with unknown senders",
            "Avoid sharing personal information"
        ]

    return explanation, advice

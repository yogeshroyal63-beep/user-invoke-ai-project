def generate_explanation(intent: str, risk: str, signals=None):

    # ---------------- LOW RISK → Reassurance ----------------
    if risk == "LOW":
        explanation = (
            "No significant malicious indicators were detected based on the current security analysis. "
            "The content appears structurally safe, but users should always remain cautious when interacting online."
        )

        advice = [
            "Verify the source before taking action",
            "Avoid sharing sensitive personal information",
            "Stay alert for unusual requests"
        ]

        return explanation, advice

    # ---------------- SCAM TEXT ----------------
    if intent == "SCAM_TEXT":
        explanation = (
            "This message contains language patterns commonly associated with scam attempts, "
            "including urgency, reward claims, or pressure tactics designed to manipulate users."
        )

        advice = [
            "Do not reply to the sender",
            "Do not click any embedded links",
            "Block and report the account",
            "Never share OTPs, passwords, or payment details"
        ]

    # ---------------- URL ----------------
    elif intent == "URL":
        explanation = (
            "This link exhibits structural or reputation-based indicators often observed in phishing "
            "or deceptive websites. Such patterns are commonly used to mislead users into revealing sensitive information."
        )

        advice = [
            "Do not open the link",
            "Avoid entering login or payment information",
            "Access official websites directly instead",
            "Delete the suspicious message"
        ]

    # ---------------- PAYMENT REQUEST ----------------
    elif intent == "PAYMENT_REQUEST":
        explanation = (
            "Requests involving urgent or unusual payments are a frequent tactic used in financial scams. "
            "Attackers often create a sense of pressure to prevent users from verifying authenticity."
        )

        advice = [
            "Do not send money immediately",
            "Verify the requester through a trusted channel",
            "Contact your bank if funds were already transferred"
        ]

    # ---------------- FILE / APP ----------------
    elif intent == "APP_OR_HASH":
        explanation = (
            "The file or application cannot be verified as safe and may contain executable or harmful components. "
            "Opening or installing unverified files can expose your system to malware risks."
        )

        advice = [
            "Do not install or execute the file",
            "Delete suspicious downloads",
            "Use official and verified app sources only"
        ]

    # ---------------- DEFAULT ----------------
    else:
        explanation = (
            "The analysis identified indicators that require caution. While not definitively malicious, "
            "certain patterns suggest potential security risk."
        )

        advice = [
            "Proceed carefully",
            "Verify authenticity before taking action",
            "Avoid sharing sensitive information"
        ]

    return explanation, advice
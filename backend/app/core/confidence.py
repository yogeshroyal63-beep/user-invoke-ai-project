def normalize_confidence(score: int, level: str = None):
    """
    Normalizes confidence score safely.
    Works with both old and new risk engine calls.
    """

    try:
        score = int(score)
    except:
        score = 0

    # If level is provided, use hybrid logic
    if level:
        if level == "HIGH":
            return max(85, min(score + 10, 99))
        elif level == "MEDIUM":
            return max(65, min(score + 5, 85))
        else:
            return max(40, min(score, 60))

    # Fallback (legacy support)
    if score >= 80:
        return 95
    if score >= 60:
        return 80
    if score >= 40:
        return 60
    return 40
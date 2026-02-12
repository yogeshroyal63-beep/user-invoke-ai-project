def compute_risk(score: float):

    if score < 0.4:
        level = "Low"
    elif score < 0.7:
        level = "Medium"
    else:
        level = "High"

    return {"score": round(score, 2), "level": level}

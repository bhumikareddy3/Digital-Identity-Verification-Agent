def fraud_score(data):
    score = 0
    if not data["aadhaar"]:
        score += 50
    if not data["pan"]:
        score += 50
    return score

def compute_confidence_score(entity):
    score = 0.0

    if entity.get("website"):
        score += 0.1

    if entity.get("linkedin"):
        score += 0.1

    if entity.get("email"):
        score += 0.1

    if entity.get("description"):
        score += 0.1

    if entity.get("founders"):
        score += 0.1

    if entity.get("technologies"):
        score += 0.1

    if entity.get("products_services"):
        score += 0.1

    if entity.get("investors"):
        score += 0.1

    if entity.get("employee_count"):
        score += 0.1

    if entity.get("hiring") is not None:
        score += 0.1

    return round(min(score, 1.0), 2)
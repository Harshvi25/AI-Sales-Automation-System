def score_lead(intent, extracted_data):

    score = 0

    # -------------------------
    # Intent Scoring
    # -------------------------

    if intent == "demo":
        score += 25

    elif intent == "pricing":
        score += 20

    elif intent == "support":
        score += 10

    # -------------------------
    # Budget Mentioned
    # -------------------------

    if extracted_data.get("budget"):
        score += 30

    # -------------------------
    # Timeline Urgency
    # -------------------------

    urgent_keywords = [
        "urgent",
        "today",
        "immediately",
        "tomorrow"
    ]

    timeline = extracted_data.get("timeline")

    if timeline in urgent_keywords:
        score += 25

    # -------------------------
    # Business Requirement
    # -------------------------

    if extracted_data.get("requirement"):
        score += 15

    # -------------------------
    # Location Mentioned
    # -------------------------

    if extracted_data.get("location"):
        score += 10

    # -------------------------
    # Priority Classification
    # -------------------------

    if score >= 70:
        priority = "HOT LEAD"

    elif score >= 40:
        priority = "MEDIUM LEAD"

    else:
        priority = "LOW LEAD"

    return {
        "lead_score": score,
        "priority": priority
    }
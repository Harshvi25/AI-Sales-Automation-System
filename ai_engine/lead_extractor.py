import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_lead_info(message):

    extracted_data = {
        "budget": None,
        "location": None,
        "requirement": None,
        "timeline": None
    }

    # -------------------------
    # Budget Extraction
    # -------------------------

    budget_pattern = r'(\d+\s?k|\d+\s?lakhs?|\d+\s?rs|\d+\s?rupees?)'

    budget_match = re.search(budget_pattern, message.lower())

    if budget_match:
        extracted_data["budget"] = budget_match.group()

    # -------------------------
    # Timeline Extraction
    # -------------------------

    timeline_keywords = [
        "today",
        "tomorrow",
        "next week",
        "next month",
        "urgent",
        "immediately"
    ]

    for word in timeline_keywords:
        if word in message.lower():
            extracted_data["timeline"] = word

    # -------------------------
    # NLP Entity Extraction
    # -------------------------

    doc = nlp(message)

    for ent in doc.ents:

        if ent.label_ == "GPE":
            extracted_data["location"] = ent.text

    # -------------------------
    # Location Keyword Fallback
    # -------------------------

    known_locations = [
        "surat",
        "ahmedabad",
        "mumbai",
        "delhi",
        "bangalore",
        "pune"
    ]

    for city in known_locations:

        if city in message.lower():

            extracted_data["location"] = city.title()

    # -------------------------
    # Requirement Extraction
    # -------------------------

    requirement_keywords = [
        "chatbot",
        "automation",
        "AI automation",
        "CRM",
        "WhatsApp bot"
    ]

    for req in requirement_keywords:
        if req.lower() in message.lower():
            extracted_data["requirement"] = req

    return extracted_data
from flask import Blueprint, request, jsonify

from ai_engine.intent_classifier import predict_intent
from ai_engine.response_generator import generate_response
from ai_engine.lead_extractor import extract_lead_info
from ai_engine.lead_scorer import score_lead
from crm.database import save_lead

receiver = Blueprint("receiver", __name__)

@receiver.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    user_message = data.get("message", "")
    user_phone = data.get("phone", "Unknown")

    print("\n==============================")
    print(f"Message from {user_phone}")
    print("==============================")

    print("User Message:", user_message)

    # -----------------------------------
    # Intent Classification
    # -----------------------------------

    intent = predict_intent(user_message)

    print("Detected Intent:", intent)

    # -----------------------------------
    # Lead Information Extraction
    # -----------------------------------

    extracted_data = extract_lead_info(user_message)

    print("Extracted Lead Data:", extracted_data)

    # -----------------------------------
    # Lead Scoring
    # -----------------------------------

    lead_result = score_lead(intent, extracted_data)

    print("Lead Analysis:", lead_result)

    # -----------------------------------
    # AI Smart Reply
    # -----------------------------------

    auto_reply = generate_response(intent)

    # -----------------------------------
    # Escalation Logic
    # -----------------------------------

    escalation = False

    if lead_result["priority"] == "HOT LEAD":
        escalation = True

    # -----------------------------------
    # Save Lead To CRM
    # -----------------------------------

    save_lead(
        user_phone,
        user_message,
        intent,
        extracted_data,
        lead_result,
        escalation
    )

    # -----------------------------------
    # Final Response
    # -----------------------------------

    response = {

        "status": "success",

        "phone": user_phone,

        "intent": intent,

        "lead_data": extracted_data,

        "lead_analysis": lead_result,

        "escalation_required": escalation,

        "auto_reply": auto_reply
    }

    return jsonify(response)
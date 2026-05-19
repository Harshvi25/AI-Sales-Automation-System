def generate_response(intent):

    responses = {

        "pricing": (
            "Thank you for your interest 😊\n"
            "Could you please share your budget and project timeline?"
        ),

        "demo": (
            "Great! We'd be happy to schedule a demo.\n"
            "Please share your preferred date and time."
        ),

        "support": (
            "We understand your issue.\n"
            "Our support/sales team will contact you shortly."
        ),

        "product_inquiry": (
            "We provide AI automation, chatbot, and business solutions.\n"
            "Could you tell us more about your requirements?"
        )

    }

    return responses.get(
        intent,
        "Thank you for contacting us. How can we assist you?"
    )
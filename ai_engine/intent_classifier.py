from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Training data
training_sentences = [

    # Pricing
    "I need pricing details",
    "What is the cost",
    "Can you share pricing",
    "What are your charges",
    "Budget for AI solution",
    "Need quotation",

    # Demo
    "Book a demo",
    "I want product demo",
    "Schedule meeting",
    "Can we arrange demo",
    "Need demo urgently",

    # Support
    "Need urgent support",
    "System is not working",
    "Facing technical issue",
    "Application crashed",
    "Need help with error",

    # Product Inquiry
    "Tell me about your AI services",
    "What solutions do you provide",
    "Need information about product",
    "Looking for AI automation",
    "Need WhatsApp chatbot",
    "Need AI solution for business"
]

training_labels = [

    # Pricing
    "pricing",
    "pricing",
    "pricing",
    "pricing",
    "pricing",
    "pricing",

    # Demo
    "demo",
    "demo",
    "demo",
    "demo",
    "demo",

    # Support
    "support",
    "support",
    "support",
    "support",
    "support",

    # Product Inquiry
    "product_inquiry",
    "product_inquiry",
    "product_inquiry",
    "product_inquiry",
    "product_inquiry",
    "product_inquiry"
]

# Vectorization
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(training_sentences)

# Model
model = LogisticRegression()

model.fit(X, training_labels)


def predict_intent(message):

    message_lower = message.lower()

    # --------------------------------
    # Business Rule Overrides
    # --------------------------------

    if "pricing" in message_lower or "budget" in message_lower:
        return "pricing"

    if "demo" in message_lower:
        return "demo"

    if "error" in message_lower or "issue" in message_lower:
        return "support"

    # --------------------------------
    # ML Prediction
    # --------------------------------

    message_vector = vectorizer.transform([message])

    prediction = model.predict(message_vector)

    return prediction[0]
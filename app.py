from flask import Flask
from webhook.receiver import receiver

from crm.database import initialize_database

app = Flask(__name__)

app.register_blueprint(receiver)

initialize_database()

@app.route("/")
def home():
    return "WhatsApp Sales AI Running Successfully"

if __name__ == "__main__":
    app.run(debug=True)
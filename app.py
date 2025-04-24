from flask import Flask
from flask_cors import CORS
from routes.recommendations import recommendation
from routes.chatbot import chatbot
import os

app = Flask(__name__)

# Configure CORS to allow requests from any origin
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

app.register_blueprint(recommendation)
app.register_blueprint(chatbot)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

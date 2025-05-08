from flask import Flask
from flask_cors import CORS
from routes.recommendations import recommendation
from routes.chatbot import chatbot

app = Flask(__name__)

# Configure CORS for the entire app
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Allow any origin
        
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Apply CORS to the recommendation blueprint
CORS(recommendation, origins="*", supports_credentials=True)

# Register blueprints
app.register_blueprint(recommendation)
app.register_blueprint(chatbot)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

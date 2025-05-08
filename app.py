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

import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS to allow requests from any origin with proper preflight handling
CORS(app, 
     resources={r"/*": {
         "origins": "*", 
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"]
     }},
     supports_credentials=True)

logger.info("CORS configured successfully")

# Add a route to handle OPTIONS requests explicitly
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 200

app.register_blueprint(recommendation)
app.register_blueprint(chatbot)

logger.info("Blueprints registered successfully")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)

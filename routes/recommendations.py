from flask import Blueprint, request, jsonify
import requests
import os

recommendation = Blueprint('recommendation', __name__)

# Use environment variable with fallback to localhost for development
AI_API_URL = os.environ.get("AI_API_URL", "http://127.0.0.1:5001/predict")

@recommendation.route('/api/predict', methods=['POST'])
def get_prediction():
    try:
        # Receive the user's input from the frontend
        data = request.json
        print("\n✅ User Input Received:", data)

        # send the data to the AI model
        ai_response = requests.post(AI_API_URL, json=data)
        ai_result = ai_response.json()

        # Added for debugging - important for now, please leave it like this
        print("🎯 AI Predicted Career:", ai_result)

        return jsonify(ai_result), ai_response.status_code

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

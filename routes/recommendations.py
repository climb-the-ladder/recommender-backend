from flask import Blueprint, request, jsonify
import requests
import os
import json

recommendation = Blueprint('recommendation', __name__)

# Get AI service URL from environment variable or use local development URL
AI_API_URL = os.getenv('AI_SERVICE_URL', 'http://localhost:5001/predict')

@recommendation.route('/api/predict', methods=['POST'])
def get_prediction():
    try:
        # Receive the user's input from the frontend
        data = request.json
        print("\n✅ User Input Received:", data)

        # send the data to the AI model
        ai_response = requests.post(AI_API_URL, json=data)
        
        # Check if the response status code is successful
        if ai_response.status_code != 200:
            return jsonify({"error": f"AI service returned status code {ai_response.status_code}"}), ai_response.status_code
            
        # Try to parse the JSON response safely
        try:
            ai_result = ai_response.json()
        except json.JSONDecodeError as e:
            print("❌ Invalid JSON response from AI service:", ai_response.text)
            return jsonify({"error": f"Invalid JSON response from AI service: {str(e)}"}), 500

        # Added for debugging - important for now, please leave it like this
        print("🎯 AI Predicted Career:", ai_result)

        return jsonify(ai_result), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

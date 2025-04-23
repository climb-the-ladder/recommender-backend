from flask import Blueprint, request, jsonify
import os
import sys
import pandas as pd
import joblib

# Add the recommender-ai directory to the Python path
sys.path.append('recommender-ai')

recommendation = Blueprint('recommendation', __name__)

# Load model directly instead of making HTTP requests
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Go up one directory to the app root

try:
    model = joblib.load(os.path.join(base_dir, "recommender-models/career_xgb.pkl"))
    scaler = joblib.load(os.path.join(base_dir, "recommender-models/scaler.pkl"))
    label_encoder = joblib.load(os.path.join(base_dir, "recommender-models/label_encoder.pkl"))
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {str(e)}")
    # We'll let the endpoint handle errors if models aren't loaded

# Expected input fields
expected_features = [
    "math_score", "history_score", "physics_score",
    "chemistry_score", "biology_score", "english_score", "geography_score"
]

@recommendation.route('/api/predict', methods=['POST'])
def get_prediction():
    try:
        # Receive the user's input from the frontend
        data = request.json
        print("\n✅ User Input Received:", data)

        # Prepare data for prediction
        features = pd.DataFrame([data])
        
        # Ensure all expected fields are present
        for feature in expected_features:
            if feature not in features:
                features[feature] = 0
                
        features = features[expected_features]
        
        # Scale the features
        features_scaled = scaler.transform(features)
        
        # Predict the career
        predicted_label = model.predict(features_scaled)[0]
        predicted_career = label_encoder.inverse_transform([predicted_label])[0]
        
        result = {"career": predicted_career}
        print("🎯 AI Predicted Career:", result)
        
        return jsonify(result), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

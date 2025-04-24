from flask import Blueprint, request, jsonify
import os
import sys
import pandas as pd
import joblib
import random

# Add the recommender-ai directory to the Python path
sys.path.append('recommender-ai')

recommendation = Blueprint('recommendation', __name__)

# Define global variables
model = None
scaler = None
label_encoder = None

# Load model directly instead of making HTTP requests
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Go up one directory to the app root

# Default career options for fallback
DEFAULT_CAREERS = [
    "Software Engineer", "Data Scientist", "Doctor", "Lawyer", 
    "Architect", "Teacher", "Accountant", "Mechanical Engineer"
]

# List all files in the recommender-models directory to help debug
try:
    model_files = os.listdir(os.path.join(base_dir, "recommender-models"))
    print(f"Files in recommender-models directory: {model_files}")
except Exception as e:
    print(f"❌ Error listing model files: {str(e)}")

# Load the models
try:
    model_path = os.path.join(base_dir, "recommender-models/career_xgb.pkl")
    scaler_path = os.path.join(base_dir, "recommender-models/scaler.pkl")
    encoder_path = os.path.join(base_dir, "recommender-models/label_encoder.pkl")
    
    print(f"Loading model from: {model_path}")
    model = joblib.load(model_path)
    
    print(f"Loading scaler from: {scaler_path}")
    scaler = joblib.load(scaler_path)
    
    print(f"Loading label encoder from: {encoder_path}")
    label_encoder = joblib.load(encoder_path)
    
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {str(e)}")
    # Models will remain None if loading fails

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

        # Check if models are loaded
        if model is None or scaler is None or label_encoder is None:
            print("⚠️ Models not loaded. Using fallback response.")
            # Return a random career as fallback
            random_career = random.choice(DEFAULT_CAREERS)
            return jsonify({"career": random_career, "note": "Using fallback response - models not loaded"}), 200
        
        # Prepare data for prediction
        features = pd.DataFrame([data])
        
        # Ensure all expected fields are present
        for feature in expected_features:
            if feature not in features:
                features[feature] = 0
                
        features = features[expected_features]
        
        # Convert string values to float
        for col in features.columns:
            features[col] = features[col].astype(float)
        
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
        # Return a fallback response on error
        random_career = random.choice(DEFAULT_CAREERS)
        return jsonify({
            "career": random_career, 
            "note": f"Error occurred, using fallback. Error: {str(e)}"
        }), 200

@recommendation.route('/api/career-details', methods=['POST'])
def get_career_details():
    try:
        data = request.json
        career = data.get('career')
        
        if not career:
            return jsonify({"error": "Career not specified"}), 400
            
        print(f"✅ Fetching details for career: {career}")
        
        # Hardcoded career details as fallback
        career_details = {
            "Software Engineer": {
                "description": "Designs, develops, and maintains software systems and applications.",
                "skills": ["Programming", "Problem Solving", "Algorithms", "Data Structures"],
                "salary_range": "$70,000 - $150,000",
                "education": "Bachelor's degree in Computer Science or related field"
            },
            "Data Scientist": {
                "description": "Analyzes and interprets complex data to help organizations make better decisions.",
                "skills": ["Statistics", "Machine Learning", "Python/R", "Data Visualization"],
                "salary_range": "$90,000 - $160,000",
                "education": "Master's or PhD in Statistics, Computer Science, or related field"
            },
            "Doctor": {
                "description": "Diagnoses and treats illnesses and injuries.",
                "skills": ["Medical Knowledge", "Diagnostic Skills", "Patient Care", "Communication"],
                "salary_range": "$150,000 - $300,000+",
                "education": "Medical Doctor (MD) degree and residency"
            },
            "Lawyer": {
                "description": "Provides legal advice and representation to individuals and organizations.",
                "skills": ["Legal Research", "Negotiation", "Analytical Thinking", "Communication"],
                "salary_range": "$70,000 - $200,000+",
                "education": "Juris Doctor (JD) degree"
            },
            "Architect": {
                "description": "Designs buildings and structures, creating plans and specifications.",
                "skills": ["Design", "Spatial Reasoning", "Technical Drawing", "Project Management"],
                "salary_range": "$60,000 - $130,000",
                "education": "Bachelor's or Master's degree in Architecture"
            },
            "Teacher": {
                "description": "Educates students in various subjects and helps them develop knowledge and skills.",
                "skills": ["Communication", "Patience", "Organization", "Subject Expertise"],
                "salary_range": "$40,000 - $90,000",
                "education": "Bachelor's degree in Education or subject area"
            },
            "Accountant": {
                "description": "Prepares and examines financial records and ensures accuracy of financial operations.",
                "skills": ["Mathematics", "Attention to Detail", "Financial Analysis", "Organization"],
                "salary_range": "$50,000 - $110,000",
                "education": "Bachelor's degree in Accounting or Finance"
            },
            "Mechanical Engineer": {
                "description": "Designs, develops, and tests mechanical devices and systems.",
                "skills": ["Mathematics", "CAD Software", "Problem Solving", "Technical Knowledge"],
                "salary_range": "$65,000 - $120,000",
                "education": "Bachelor's degree in Mechanical Engineering"
            }
        }
        
        # Return the details for the requested career, or a default response if not found
        if career in career_details:
            return jsonify(career_details[career]), 200
        else:
            # Generic details for any career not in our hardcoded list
            return jsonify({
                "description": f"Professional in the field of {career}.",
                "skills": ["Relevant technical skills", "Communication", "Problem solving"],
                "salary_range": "Varies based on experience and location",
                "education": "Related degree or certification"
            }), 200
            
    except Exception as e:
        print(f"❌ Error in career details: {str(e)}")
        return jsonify({
            "description": "Information temporarily unavailable.",
            "error": str(e)
        }), 200

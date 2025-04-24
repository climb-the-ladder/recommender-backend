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
                "education": "Bachelor's degree in Computer Science or related field",
                "difficulty": 7,
                "job_outlook": "Excellent growth projected over the next decade with increasing demand for software solutions.",
                "day_to_day": "Writing code, debugging, attending meetings, collaborating with team members, and testing applications.",
                "advancement": "Can progress to senior developer, technical lead, architect, or management roles.",
                "work_life_balance": {
                    "rating": 7,
                    "explanation": "Generally good balance, though may require occasional overtime during project deadlines."
                },
                "pros": ["High demand", "Good compensation", "Remote work options", "Creative problem solving"],
                "cons": ["Can be stressful during deadlines", "Requires continuous learning", "Some positions have long hours"]
            },
            "Data Scientist": {
                "description": "Analyzes and interprets complex data to help organizations make better decisions.",
                "skills": ["Statistics", "Machine Learning", "Python/R", "Data Visualization"],
                "salary_range": "$90,000 - $160,000",
                "education": "Master's or PhD in Statistics, Computer Science, or related field",
                "difficulty": 8,
                "job_outlook": "Strong growth expected as businesses increasingly rely on data-driven decision making.",
                "day_to_day": "Analyzing data, building models, creating visualizations, presenting findings to stakeholders.",
                "advancement": "Can advance to senior data scientist, lead data scientist, or management positions.",
                "work_life_balance": {
                    "rating": 8,
                    "explanation": "Generally good work-life balance with flexible hours in many organizations."
                },
                "pros": ["Intellectually stimulating", "High demand", "Good compensation", "Opportunity to make business impact"],
                "cons": ["Requires extensive education", "Can be challenging to explain complex concepts", "May involve cleaning messy data"]
            },
            "Doctor": {
                "description": "Diagnoses and treats illnesses and injuries.",
                "skills": ["Medical Knowledge", "Diagnostic Skills", "Patient Care", "Communication"],
                "salary_range": "$150,000 - $300,000+",
                "education": "Medical Doctor (MD) degree and residency",
                "difficulty": 9,
                "job_outlook": "Consistent demand with growth in specialized fields and aging population needs.",
                "day_to_day": "Patient consultations, diagnoses, treatments, record-keeping, continuing education.",
                "advancement": "Can specialize in various fields, become a department head, or open a private practice.",
                "work_life_balance": {
                    "rating": 5,
                    "explanation": "Often challenging with long hours, especially during residency and for certain specialties."
                },
                "pros": ["Respected profession", "High compensation", "Opportunity to help others", "Job security"],
                "cons": ["Long training period", "High stress", "Long hours", "High stakes decisions"]
            },
            "Lawyer": {
                "description": "Provides legal advice and representation to individuals and organizations.",
                "skills": ["Legal Research", "Negotiation", "Analytical Thinking", "Communication"],
                "salary_range": "$70,000 - $200,000+",
                "education": "Juris Doctor (JD) degree",
                "difficulty": 8,
                "job_outlook": "Steady demand with growth in areas like intellectual property and healthcare law.",
                "day_to_day": "Client meetings, legal research, drafting documents, negotiations, court appearances.",
                "advancement": "Can become a partner in a firm, specialize in a legal area, or become a judge.",
                "work_life_balance": {
                    "rating": 6,
                    "explanation": "Often demanding hours, especially in large firms, though some specialties offer better balance."
                },
                "pros": ["Intellectually challenging", "Potential for high income", "Prestigious career", "Opportunity to help others"],
                "cons": ["Long hours", "High stress", "Competitive field", "Extensive education requirements"]
            },
            "Architect": {
                "description": "Designs buildings and structures, creating plans and specifications.",
                "skills": ["Design", "Spatial Reasoning", "Technical Drawing", "Project Management"],
                "salary_range": "$60,000 - $130,000",
                "education": "Bachelor's or Master's degree in Architecture",
                "difficulty": 7,
                "job_outlook": "Moderate growth tied to construction industry trends and economic conditions.",
                "day_to_day": "Creating designs, drafting plans, meeting with clients, coordinating with engineers and contractors.",
                "advancement": "Can progress to senior architect, partner, or start own firm.",
                "work_life_balance": {
                    "rating": 7,
                    "explanation": "Generally reasonable hours, though deadlines can require occasional overtime."
                },
                "pros": ["Creative expression", "Seeing designs become reality", "Varied projects", "Blend of art and science"],
                "cons": ["Long education and licensure process", "Affected by economic cycles", "Competitive field"]
            },
            "Teacher": {
                "description": "Educates students in various subjects and helps them develop knowledge and skills.",
                "skills": ["Communication", "Patience", "Organization", "Subject Expertise"],
                "salary_range": "$40,000 - $90,000",
                "education": "Bachelor's degree in Education or subject area",
                "difficulty": 7,
                "job_outlook": "Stable demand with regional variations; growing need in STEM subjects.",
                "day_to_day": "Lesson planning, teaching classes, grading assignments, meeting with students and parents.",
                "advancement": "Can become department head, administrator, curriculum developer, or educational consultant.",
                "work_life_balance": {
                    "rating": 7,
                    "explanation": "Regular schedule with summers off, though often involves after-hours work grading and planning."
                },
                "pros": ["Making a difference in students' lives", "Job security", "Regular schedule", "Breaks during the year"],
                "cons": ["Can be emotionally demanding", "Moderate compensation", "Administrative challenges", "Need to handle difficult classroom situations"]
            },
            "Accountant": {
                "description": "Prepares and examines financial records and ensures accuracy of financial operations.",
                "skills": ["Mathematics", "Attention to Detail", "Financial Analysis", "Organization"],
                "salary_range": "$50,000 - $110,000",
                "education": "Bachelor's degree in Accounting or Finance",
                "difficulty": 7,
                "job_outlook": "Stable demand with consistent need for financial expertise in all sectors.",
                "day_to_day": "Analyzing financial data, preparing reports, ensuring regulatory compliance, auditing records.",
                "advancement": "Can progress to senior accountant, controller, financial manager, or partner in a firm.",
                "work_life_balance": {
                    "rating": 6,
                    "explanation": "Generally good, though tax season can be demanding with long hours."
                },
                "pros": ["Job stability", "Clear career path", "Variety of industries to work in", "Analytical work"],
                "cons": ["Seasonal workload fluctuations", "Keeping up with changing regulations", "Can be repetitive"]
            },
            "Mechanical Engineer": {
                "description": "Designs, develops, and tests mechanical devices and systems.",
                "skills": ["Mathematics", "CAD Software", "Problem Solving", "Technical Knowledge"],
                "salary_range": "$65,000 - $120,000",
                "education": "Bachelor's degree in Mechanical Engineering",
                "difficulty": 8,
                "job_outlook": "Steady demand across manufacturing, automotive, aerospace, and energy sectors.",
                "day_to_day": "Designing mechanical systems, testing prototypes, analyzing test data, collaborating with other engineers.",
                "advancement": "Can become senior engineer, engineering manager, or technical specialist.",
                "work_life_balance": {
                    "rating": 7,
                    "explanation": "Generally good balance with standard hours, though project deadlines may require overtime."
                },
                "pros": ["Problem-solving challenges", "Tangible results", "Diverse applications", "Good compensation"],
                "cons": ["Requires continuous learning", "Complex problems", "Manufacturing jobs may be affected by economic cycles"]
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
                "education": "Related degree or certification",
                "difficulty": 7,
                "job_outlook": "Varies by region and economic conditions.",
                "day_to_day": "Performing tasks related to the profession, collaborating with colleagues, and developing expertise.",
                "advancement": "Career progression typically involves gaining expertise and taking on more responsibility.",
                "work_life_balance": {
                    "rating": 7,
                    "explanation": "Balance varies depending on employer and specific role."
                },
                "pros": ["Career growth opportunities", "Professional development", "Applying specialized knowledge"],
                "cons": ["May require continued education", "Competitive job market", "Industry-specific challenges"]
            }), 200
            
    except Exception as e:
        print(f"❌ Error in career details: {str(e)}")
        return jsonify({
            "description": "Information temporarily unavailable.",
            "skills": ["Information not available"],
            "salary_range": "Information not available",
            "education": "Information not available",
            "difficulty": 5,
            "job_outlook": "Information not available",
            "day_to_day": "Information not available",
            "advancement": "Information not available",
            "work_life_balance": {
                "rating": 5,
                "explanation": "Information not available"
            },
            "pros": ["Information not available"],
            "cons": ["Information not available"]
        }), 200

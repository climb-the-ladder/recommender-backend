import sys
import os
from flask import Blueprint, request, jsonify
import requests

# Add recommender-ai to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../recommender-ai')))

from chatbot import CareerChatbot
from gpt_chatbot import handle_chat
from career_roadmap import generate_career_roadmap
from university_summaries import university_summary_generator
from alternative_careers import AlternativeCareersAnalyzer

chatbot = Blueprint('chatbot', __name__)
career_chatbot = CareerChatbot()
alternative_careers_analyzer = AlternativeCareersAnalyzer()

@chatbot.route('/api/chatbot-recommend', methods=['POST'])
def chatbot_recommend():
    data = request.json
    career = data.get('career')

    if not career:
        return jsonify({"error": "Missing career"}), 400

    similar_careers = alternative_careers_analyzer.get_similar_careers(career)
    
    return jsonify({
        "similar_careers": similar_careers[:5]  # Limit to top 5 alternatives
    })

@chatbot.route('/api/analyze-careers', methods=['POST'])
def analyze_careers():
    data = request.json
    careers = data.get('careers', [])
    academic_scores = data.get('academic_scores', {})
    predicted_career = data.get('predicted_career')

    if not careers or not academic_scores or not predicted_career:
        return jsonify({"error": "Missing required data"}), 400

    try:
        analyzed_careers = []
        for career in careers:
            analysis = alternative_careers_analyzer.analyze_career_match(
                career, 
                academic_scores, 
                predicted_career
            )
            analyzed_careers.append({
                "career": career,
                "matching_score": analysis["matching_score"],
                "explanation": analysis["explanation"],
                "key_skills": analysis["key_skills"]
            })

        # Sort by matching score
        analyzed_careers.sort(key=lambda x: x["matching_score"], reverse=True)
        
        return jsonify({
            "success": True,
            "analyzed_careers": analyzed_careers
        })
    except Exception as e:
        error_msg = f"Failed to analyze careers: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg, "success": False}), 500

@chatbot.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    career = data.get('career')
    gpa = data.get('gpa')
    subject_grades = data.get('subject_grades', {})
    session_id = data.get('session_id', 'default')
    
    if not message:
        return jsonify({"error": "Missing message"}), 400
    
    # Call the handle_chat function with all parameters including subject_grades
    response = handle_chat(message, career, gpa, subject_grades, session_id)
    
    return jsonify({"response": response})

@chatbot.route('/api/career-details', methods=['POST'])
def get_career_details():
    data = request.json
    career = data.get('career')
    
    print(f"Career details requested for: {career}")

    if not career:
        return jsonify({"error": "Missing career"}), 400

    try:
        print(f"Forwarding request to AI service for career: {career}")
        # Forward the request to the AI service
        response = requests.post(
            'http://localhost:5001/career-details',
            json={"career": career},
            timeout=60  # Increased timeout for GPT responses
        )
        response.raise_for_status()
        result = response.json()
        print(f"Received response from AI service: {result.get('success', False)}")
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to get career details: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg, "success": False}), 500

@chatbot.route('/api/career-roadmap', methods=['POST'])
def get_career_roadmap():
    data = request.json
    career = data.get('career')
    subject_grades = data.get('subject_grades', {})
    gpa = data.get('gpa')
    
    print(f"Career roadmap requested for: {career}")

    if not career:
        return jsonify({"error": "Missing career", "success": False}), 400

    try:
        # Call the generate_career_roadmap function
        result = generate_career_roadmap(career, subject_grades, gpa)
        return jsonify(result)
    except Exception as e:
        error_msg = f"Failed to generate career roadmap: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg, "success": False}), 500

@chatbot.route('/api/university-summary', methods=['POST'])
def get_university_summary():
    data = request.json
    university_name = data.get('university_name')
    additional_info = data.get('additional_info', {})
    
    if not university_name:
        return jsonify({"error": "Missing university name", "success": False}), 400

    try:
        summary = university_summary_generator.generate_summary(university_name, additional_info)
        return jsonify({
            "success": True,
            "summary": {
                "overview": summary["overview"],
                "academic_programs": summary["academic_programs"],
                "campus_life": summary["campus_life"],
                "achievements": summary["achievements"],
                "unique_features": summary["unique_features"]
            }
        })
    except Exception as e:
        error_msg = f"Failed to generate university summary: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({"error": error_msg, "success": False}), 500

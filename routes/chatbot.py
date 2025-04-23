import sys
import os
from flask import Blueprint, request, jsonify
import requests

# Add recommender-ai to the system path
sys.path.append('recommender-ai')

from chatbot import CareerChatbot
from gpt_chatbot import handle_chat

chatbot = Blueprint('chatbot', __name__)
career_chatbot = CareerChatbot()

@chatbot.route('/api/chatbot-recommend', methods=['POST'])
def chatbot_recommend():
    data = request.json
    gpa = data.get('gpa')
    career = data.get('career')

    if not gpa or not career:
        return jsonify({"error": "Missing GPA or career"}), 400

    unis, similar_careers = career_chatbot.recommend(float(gpa), career)

    return jsonify({
        "recommended_universities": unis,
        "similar_careers": similar_careers
    })

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

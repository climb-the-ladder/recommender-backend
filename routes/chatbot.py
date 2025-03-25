import sys
import os
from flask import Blueprint, request, jsonify

# Add recommender-ai to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../recommender-ai')))

from chatbot import CareerChatbot  # ✅ Import works now

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

from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import dotenv

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Fallback data
fallback_careers = ["Software Engineer", "Data Scientist", "Product Manager", "UX Designer"]

# Optional dependencies
pandas_available = False
requests_available = False
sqlite_available = False
conn = None
cursor = None

# Try importing pandas
try:
    import pandas as pd
    pandas_available = True
except ImportError:
    print("Warning: pandas not available")

# Try importing requests
try:
    import requests
    requests_available = True
except ImportError:
    print("Warning: requests not available")

# Try importing sqlite and setting up the database
try:
    import sqlite3
    sqlite_available = True
    
    # Connect to database
    conn = sqlite3.connect("user_history.db", check_same_thread=False)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gpa REAL,
            coding_skills INTEGER,
            communication_skills INTEGER,
            recommended_career TEXT
        )
    """)
    conn.commit()
except Exception as e:
    print(f"Database setup error: {str(e)}")

# Configure AI service URL
AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL", "http://localhost:5001/predict")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.json
        
        # If requests module isn't available, use fallback
        if not requests_available:
            import random
            career = random.choice(fallback_careers)
            return jsonify({"recommended_career": career, "note": "Using fallback (requests not available)"})
        
        # Forward the request to the AI service
        ai_response = requests.post(AI_SERVICE_URL, json=data, timeout=10)
        
        if ai_response.status_code != 200:
            return jsonify({"error": "AI service error", "status": ai_response.status_code}), 500
            
        ai_result = ai_response.json()
        career = ai_result.get("career")
        
        # Save to database if SQLite is available
        if sqlite_available and conn and cursor:
            try:
                cursor.execute(
                    "INSERT INTO recommendations (gpa, coding_skills, communication_skills, recommended_career) VALUES (?, ?, ?, ?)", 
                    (data.get("gpa", 0), data.get("coding", 0), data.get("communication", 0), career)
                )
                conn.commit()
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
        
        return jsonify({"recommended_career": career})
    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        import random
        return jsonify({
            "recommended_career": random.choice(fallback_careers), 
            "error": str(e),
            "note": "Using fallback due to error"
        })

@app.route("/health", methods=["GET"])
def health_check():
    # Check if AI service is available
    ai_available = False
    if requests_available:
        try:
            health_url = AI_SERVICE_URL.replace("/predict", "/health")
            ai_health = requests.get(health_url, timeout=2)
            ai_available = ai_health.status_code == 200
        except:
            pass
            
    return jsonify({
        "status": "ok",
        "dependencies": {
            "pandas": pandas_available,
            "requests": requests_available,
            "sqlite": sqlite_available
        },
        "ai_service_available": ai_available
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    # Check if we're in production or development
    debug_mode = os.environ.get("FLASK_ENV", "development") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

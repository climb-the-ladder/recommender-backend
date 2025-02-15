from flask import Flask, request, jsonify
import joblib
import os
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect("user_history.db")
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

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    features = pd.DataFrame([data])
    career = model.predict(features)[0]

    # Save to database
    cursor.execute("INSERT INTO recommendations (gpa, coding_skills, communication_skills, recommended_career) VALUES (?, ?, ?, ?)", 
                   (data["GPA"], data["Coding_Skills"], data["Communication_Skills"], career))
    conn.commit()

    return jsonify({"recommended_career": career})


app = Flask(__name__)

#w load trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "../recommender-models/career_recommender.pkl")
model = joblib.load(model_path)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json  # Get JSON data from request
    features = pd.DataFrame([data])  # Convert input to DataFrame
    career = model.predict(features)[0]  # Make prediction
    return jsonify({"recommended_career": career})  # Return response

if __name__ == "__main__":
    app.run(debug=True)

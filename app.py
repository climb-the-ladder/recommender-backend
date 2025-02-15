from flask import Flask, request, jsonify
import joblib
import os
import pandas as pd

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

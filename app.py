from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), "../recommender-models/career_recommender.pkl")
model = joblib.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get JSON data from the request
    user_data = pd.DataFrame([data])  # Convert to DataFrame

    #redict probabilities for all career classes
    probabilities = model.predict_proba(user_data)[0]
    career_classes = model.classes_

    # Prepare top 3 career predictions (now we only predict 1 for the moment in tests)
    predictions = sorted(
        zip(career_classes, probabilities), key=lambda x: x[1], reverse=True
    )[:3]

    response = [{"career": career, "probability": round(prob * 100, 2)} for career, prob in predictions]
    return jsonify({"predictions": response})

if __name__ == '__main__':
    app.run(port=5001, debug=True)

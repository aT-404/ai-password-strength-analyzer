import joblib
import pandas as pd
import numpy as np
import re
from flask import Flask, request, jsonify
from flask_cors import CORS 
import os

app = Flask(__name__)
CORS(app) 

# IMPORTANT: You must update the API_URL in index.html when you deploy this to a public server!
MODEL = None
FEATURE_NAMES = None
CLASS_LABELS = {0: "Weak", 1: "Medium", 2: "Strong"}
MODEL_PATH = 'password_strength_model.joblib'
FEATURES_PATH = 'model_features.joblib'

def load_model_assets():
    global MODEL, FEATURE_NAMES
    if not os.path.exists(MODEL_PATH) or not os.path.exists(FEATURES_PATH):
        print(f"Error: Model files not found. Run password_model_trainer.py first.")
        return False
        
    try:
        MODEL = joblib.load(MODEL_PATH)
        FEATURE_NAMES = joblib.load(FEATURES_PATH)
        print("Model and feature list loaded.")
        return True
    except Exception as e:
        print(f"Error loading model assets: {e}")
        return False

# --- Feature Extraction Function (Must match training features) ---
def get_features(password):
    features = {
        'length': len(password),
        'has_lower': int(bool(re.search(r'[a-z]', password))),
        'has_upper': int(bool(re.search(r'[A-Z]', password))),
        'has_digit': int(bool(re.search(r'\d', password))),
        'has_special': int(bool(re.search(r'[^a-zA-Z0-9\s]', password))),
    }
    features['diversity_score'] = features['has_lower'] + features['has_upper'] + features['has_digit'] + features['has_special']
    features['entropy_heuristic'] = features['length'] * features['diversity_score']
    features['min_length_ok'] = int(features['length'] >= 8)
    features['min_diversity_ok'] = int(features['has_upper'] and features['has_lower'] and features['has_digit'])
            
    return features

@app.route('/predict', methods=['POST'])
def predict_strength():
    if MODEL is None or FEATURE_NAMES is None:
        return jsonify({"error": "Model not loaded. Check server logs."}), 500

    try:
        data = request.get_json(force=True)
        password = data.get('password')
        if not password:
            return jsonify({"error": "No password provided."}), 400

        raw_features = get_features(password)
        input_data = pd.DataFrame([raw_features], columns=FEATURE_NAMES)
        
        prediction_class = MODEL.predict(input_data)[0]
        probabilities = MODEL.predict_proba(input_data)[0]
        confidence = probabilities[prediction_class]
        
        result = {
            "password": password,
            "strength": CLASS_LABELS.get(prediction_class, "Unknown"),
            "confidence": f"{confidence * 100:.2f}%",
            "details": {
                "length": raw_features['length'],
                "diversity_score": raw_features['diversity_score'],
                "has_special": bool(raw_features['has_special']),
                "entropy_heuristic": raw_features['entropy_heuristic']
            }
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

if __name__ == '__main__':
    if load_model_assets():
        app.run(host='0.0.0.0', port=5000)
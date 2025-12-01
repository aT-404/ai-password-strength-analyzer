🔐 AI-Powered Password Strength Analyzer

This project is a full-stack application demonstrating the power of Machine Learning in Cybersecurity. It classifies passwords into Weak, Medium, or Strong in real-time using a trained Random Forest model based on feature-engineered metrics.

➡️ Live Demo: [Insert Deployment Link Here] (Will be updated after hosting)

✨ Features

Intelligent Classification: Uses a trained Machine Learning model (scikit-learn Random Forest).

Feature Engineering: Scores passwords based on entropy, diversity, and length.

Real-Time API: A lightweight Flask API handles prediction requests.

Modern Frontend: Responsive web interface built with Vanilla JavaScript and Tailwind CSS.

⚙️ Local Setup Instructions

1. Prerequisites

pip install pandas scikit-learn flask flask-cors joblib numpy


2. Run the Data Pipeline (Generate Files)

You must run these two scripts in your project folder to create the necessary local data and model files (.csv, .joblib) before starting the API.

# 1. Generate data and extract features
python password_data_generator.py

# 2. Train the ML model and save the assets
python password_model_trainer.py


3. Run the Backend API

python api_endpoint.py


4. Run the Frontend

Open the index.html file in your browser or a live server. The frontend is configured to communicate with the local Flask API.
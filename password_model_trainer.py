import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

def train_and_save_model():
    data_file = 'password_data.csv'
    if not os.path.exists(data_file):
        print(f"Error: Required file '{data_file}' not found.")
        print("Please run 'password_data_generator.py' first.")
        return

    print(f"Loading data from {data_file}...")
    df = pd.read_csv(data_file)

    X = df.drop(columns=['strength_class'])
    Y = df['strength_class']
    
    feature_names = X.columns.tolist()
    joblib.dump(feature_names, 'model_features.joblib')
    print("Saved feature names to 'model_features.joblib'.")

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42, stratify=Y
    )

    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, Y_train)
    print("Training complete.")

    Y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    class_labels = ['Weak', 'Medium', 'Strong']
    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:\n", classification_report(Y_test, Y_pred, target_names=class_labels))

    model_filename = 'password_strength_model.joblib'
    joblib.dump(model, model_filename)
    print(f"Successfully saved model to '{model_filename}'.")


if __name__ == '__main__':
    train_and_save_model()
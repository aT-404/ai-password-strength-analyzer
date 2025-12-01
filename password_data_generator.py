import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# --- Data Generation ---

def generate_raw_passwords():
    """Generates a sample dataset of passwords with simulated strength scores."""
    data = [
        # Weak (Score 0-3)
        ("123456", 1), ("password", 1), ("qwerty", 0), ("summer2024", 2),
        ("albert5", 2), ("Albert1", 3), ("iloveyou", 1), ("kottayam", 1),
        # Medium (Score 4-6)
        ("SecurePwd123", 4), ("MyP@ssw0rd!", 5), ("Robot_Control_V1", 6),
        ("PyThOnR0cks", 5), ("firebaseDB4", 4), ("moveit_planner", 6),
        # Strong (Score 7-10)
        ("A1bertT0jK#yY@l@", 8), ("R0S2_Gazebo_Sim_P1an", 9),
        ("Th3CyB3rS3cur1tyGrind!", 10), ("Cr3@t1v3Pr0bl3mS0lv3r!", 9),
        ("AIML_R0b0tic5_2027#", 10), ("Complex_puzzl3s_404_!", 8)
    ]
    # Expand data for a larger sample set for training
    df_raw = pd.DataFrame(data * 50, columns=['password', 'strength_score'])
    df_raw = df_raw.sample(frac=1).reset_index(drop=True)
    
    # Map raw scores to classes (0: Weak, 1: Medium, 2: Strong)
    def map_score_to_class(score):
        if score <= 3: return 0
        if score <= 6: return 1
        return 2
    
    df_raw['strength_class'] = df_raw['strength_score'].apply(map_score_to_class)
    return df_raw

# --- Feature Engineering (Core of the Project) ---

def get_features(password):
    """Extracts numerical and Boolean features from a single password string."""
    features = {
        'length': len(password),
        'has_lower': bool(re.search(r'[a-z]', password)),
        'has_upper': bool(re.search(r'[A-Z]', password)),
        'has_digit': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[^a-zA-Z0-9\s]', password)),
    }
    # Calculate diversity score from the boolean checks
    diversity_score = (
        features['has_lower'] + 
        features['has_upper'] + 
        features['has_digit'] + 
        features['has_special']
    )
    features['diversity_score'] = diversity_score
    
    # Simple entropy heuristic
    features['entropy_heuristic'] = len(password) * diversity_score
    
    # Threshold checks
    features['min_length_ok'] = features['length'] >= 8
    features['min_diversity_ok'] = (features['has_upper'] and features['has_lower'] and features['has_digit'])

    return features

def process_password_data(df):
    """Applies feature extraction to the entire dataset and prepares for ML."""
    feature_list = df['password'].apply(lambda x: pd.Series(get_features(x)))
    df_final = pd.concat([df.drop(columns=['strength_score']), feature_list], axis=1)
    
    # Convert boolean columns to integer (1 or 0) for the ML model
    bool_cols = [col for col in df_final.columns if df_final[col].dtype == 'bool']
    for col in bool_cols:
        df_final[col] = df_final[col].astype(int)
        
    return df_final.drop(columns=['password'])

if __name__ == '__main__':
    raw_df = generate_raw_passwords()
    processed_df = process_password_data(raw_df)
    processed_df.to_csv('password_data.csv', index=False)
    print("Data preparation complete. 'password_data.csv' saved.")
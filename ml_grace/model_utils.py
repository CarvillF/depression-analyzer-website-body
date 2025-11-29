"""
Utility functions for loading ML models and making predictions.
This module provides a simple interface for the web applications.
"""

import pickle
import pandas as pd
import os

# Cache for loaded models
_models_cache = None

def load_models():
    """
    Load both trained models and their metadata.
    Returns a dictionary containing models and configuration.
    """
    global _models_cache
    
    if _models_cache is not None:
        return _models_cache
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load depression model
    with open(os.path.join(script_dir, 'depression_model.pkl'), 'rb') as f:
        depression_model = pickle.load(f)
    
    # Load suicidal thoughts model
    with open(os.path.join(script_dir, 'suicidal_model.pkl'), 'rb') as f:
        suicidal_model = pickle.load(f)
    
    # Load model info from the new separate info files
    with open(os.path.join(script_dir, 'depression_model_info.pkl'), 'rb') as f:
        depression_info = pickle.load(f)
    
    with open(os.path.join(script_dir, 'suicidal_model_info.pkl'), 'rb') as f:
        suicidal_info = pickle.load(f)
    
    # Create unified model info structure for backward compatibility
    model_info = {
        'depression_features': depression_info['feature_columns'],
        'suicidal_features': suicidal_info['feature_columns'],
        'encodings': {
            'Gender': {'Male': 0, 'Female': 1},
            'Sleep Duration': {
                'Less than 5 hours': 1,
                '5-6 hours': 2,
                '7-8 hours': 3,
                'More than 8 hours': 4
            },
            'Dietary Habits': {'Unhealthy': 1, 'Moderate': 2, 'Healthy': 3},
            'Have you ever had suicidal thoughts ?': {'No': 0, 'Yes': 1},
            'Family History of Mental Illness': {'No': 0, 'Yes': 1},
            'Depression': {'No': 0, 'Yes': 1}
        },
        'feature_order': depression_info['feature_columns'],
        'depression_accuracy': depression_info['accuracy'],
        'suicidal_accuracy': suicidal_info['accuracy']
    }
    
    _models_cache = {
        'depression_model': depression_model,
        'suicidal_model': suicidal_model,
        'info': model_info
    }
    
    return _models_cache


def preprocess_input(gender, age, academic_pressure, study_satisfaction,
                     sleep_duration, dietary_habits, study_hours,
                     financial_stress, family_history):
    """
    Convert raw web form inputs into the format expected by models.
    
    Args:
        gender: "Male" or "Female"
        age: int (18-34)
        academic_pressure: float (1-5)
        study_satisfaction: float (1-5)
        sleep_duration: str or int (dropdown text or encoded value)
        dietary_habits: str or int (dropdown text or encoded value)
        study_hours: int
        financial_stress: float (1-5)
        family_history: "Yes" or "No"
    
    Returns:
        pandas DataFrame with encoded features
    """
    models = load_models()
    encodings = models['info']['encodings']
    
    # Handle gender encoding
    if isinstance(gender, str):
        gender_encoded = encodings['Gender'].get(gender, 0)
    else:
        gender_encoded = gender
    
    # Handle sleep duration encoding
    if isinstance(sleep_duration, str):
        # Map common variations
        sleep_map = {
            'Less than 5 hours': 1,
            'Less than 5 h': 1,
            '5-6 hours': 2,
            '5-6 h': 2,
            '7-8 hours': 3,
            '7-8 h': 3,
            'More than 8 hours': 4,
            'More than 8 h': 4
        }
        sleep_encoded = sleep_map.get(sleep_duration, 3)  # Default to 7-8 hours
    else:
        sleep_encoded = sleep_duration
    
    # Handle dietary habits encoding
    if isinstance(dietary_habits, str):
        diet_map = {
            'Unhealthy': 1,
            'Moderate': 2,
            'Healthy': 3
        }
        diet_encoded = diet_map.get(dietary_habits, 2)  # Default to Moderate
    else:
        diet_encoded = dietary_habits
    
    # Handle family history encoding
    if isinstance(family_history, str):
        family_encoded = encodings['Family History of Mental Illness'].get(family_history, 0)
    else:
        family_encoded = family_history
    
    # Create DataFrame with features in correct order
    feature_data = {
        'Gender': gender_encoded,
        'Age': int(age),
        'Academic Pressure': float(academic_pressure),
        'Study Satisfaction': float(study_satisfaction),
        'Sleep Duration': sleep_encoded,
        'Dietary Habits': diet_encoded,
        'Study Hours': int(study_hours),
        'Financial Stress': float(financial_stress),
        'Family History of Mental Illness': family_encoded
    }
    
    return pd.DataFrame([feature_data])


def predict_depression(gender, age, academic_pressure, study_satisfaction,
                       sleep_duration, dietary_habits, study_hours,
                       financial_stress, family_history):
    """
    Predict depression risk.
    
    Returns:
        tuple: (prediction, probability_no_depression, probability_depression)
    """
    models = load_models()
    
    # Preprocess input
    input_df = preprocess_input(
        gender, age, academic_pressure, study_satisfaction,
        sleep_duration, dietary_habits, study_hours,
        financial_stress, family_history
    )
    
    # Make prediction
    prediction = models['depression_model'].predict(input_df)[0]
    probabilities = models['depression_model'].predict_proba(input_df)[0]
    
    return prediction, probabilities[0], probabilities[1]


def predict_suicidal_thoughts(gender, age, academic_pressure, study_satisfaction,
                               sleep_duration, dietary_habits, study_hours,
                               financial_stress, family_history):
    """
    Predict suicidal thoughts risk.
    
    Returns:
        tuple: (prediction, probability_no, probability_yes)
    """
    models = load_models()
    
    # Preprocess input
    input_df = preprocess_input(
        gender, age, academic_pressure, study_satisfaction,
        sleep_duration, dietary_habits, study_hours,
        financial_stress, family_history
    )
    
    # Make prediction
    prediction = models['suicidal_model'].predict(input_df)[0]
    probabilities = models['suicidal_model'].predict_proba(input_df)[0]
    
    return prediction, probabilities[0], probabilities[1]


def predict_both(gender, age, academic_pressure, study_satisfaction,
                 sleep_duration, dietary_habits, study_hours,
                 financial_stress, family_history):
    """
    Predict both depression and suicidal thoughts risk.
    
    Returns:
        dict with keys:
            - depression_prediction: 0 or 1
            - depression_probability: float (0-1)
            - suicidal_prediction: 0 or 1
            - suicidal_probability: float (0-1)
    """
    dep_pred, dep_prob_no, dep_prob_yes = predict_depression(
        gender, age, academic_pressure, study_satisfaction,
        sleep_duration, dietary_habits, study_hours,
        financial_stress, family_history
    )
    
    sui_pred, sui_prob_no, sui_prob_yes = predict_suicidal_thoughts(
        gender, age, academic_pressure, study_satisfaction,
        sleep_duration, dietary_habits, study_hours,
        financial_stress, family_history
    )
    
    return {
        'depression_prediction': dep_pred,
        'depression_probability': dep_prob_yes,
        'suicidal_prediction': sui_pred,
        'suicidal_probability': sui_prob_yes
    }

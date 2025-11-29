"""
Train Random Forest models for depression and suicidal thoughts prediction.
This script creates two separate models and saves them as pickle files.
"""

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os

# Configuration
DATA_PATH = 'Depression Student Dataset.csv'
TEST_RATIO = 0.3
NUM_TREES = 1000
RANDOM_STATE = 42

print("=" * 60)
print("Mental Health Prediction Model Training")
print("=" * 60)

# Load the data
print("\n[1/6] Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"   ✓ Loaded {len(df)} records with {len(df.columns)} columns")

# Store original mappings for later use
print("\n[2/6] Creating label encodings...")
encodings = {
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
}

# Apply encodings
df_encoded = df.copy()
for column, mapping in encodings.items():
    if column in df_encoded.columns:
        df_encoded[column] = df_encoded[column].map(mapping)

print("   ✓ Applied label encoding to categorical features")

# ============================================================================
# Model 1: Depression Prediction (without Suicidal Thoughts as feature)
# ============================================================================
print("\n[3/6] Training Depression Prediction Model...")
print("-" * 60)

# Features: everything except Depression and Suicidal Thoughts
depression_features = [
    'Gender', 'Age', 'Academic Pressure', 'Study Satisfaction',
    'Sleep Duration', 'Dietary Habits', 'Study Hours',
    'Financial Stress', 'Family History of Mental Illness'
]

X_depression = df_encoded[depression_features]
y_depression = df_encoded['Depression']

# Split data
X_train_dep, X_test_dep, y_train_dep, y_test_dep = train_test_split(
    X_depression, y_depression, test_size=TEST_RATIO, random_state=RANDOM_STATE
)

# Train model
depression_model = RandomForestClassifier(
    n_estimators=NUM_TREES, 
    random_state=RANDOM_STATE
)
depression_model.fit(X_train_dep, y_train_dep)

# Evaluate
y_pred_dep = depression_model.predict(X_test_dep)
accuracy_dep = accuracy_score(y_test_dep, y_pred_dep)

print(f"\n   Depression Model Performance:")
print(f"   Accuracy: {accuracy_dep * 100:.2f}%")
print(f"\n   Confusion Matrix:")
print(f"   {confusion_matrix(y_test_dep, y_pred_dep)}")
print(f"\n   Classification Report:")
print(classification_report(y_test_dep, y_pred_dep, target_names=['No Depression', 'Depression']))

# Save model
with open('depression_model.pkl', 'wb') as f:
    pickle.dump(depression_model, f)
print("\n   ✓ Saved depression_model.pkl")

# ============================================================================
# Model 2: Suicidal Thoughts Prediction (without Depression as feature)
# ============================================================================
print("\n[4/6] Training Suicidal Thoughts Prediction Model...")
print("-" * 60)

# Features: everything except Depression and Suicidal Thoughts
suicidal_features = [
    'Gender', 'Age', 'Academic Pressure', 'Study Satisfaction',
    'Sleep Duration', 'Dietary Habits', 'Study Hours',
    'Financial Stress', 'Family History of Mental Illness'
]

X_suicidal = df_encoded[suicidal_features]
y_suicidal = df_encoded['Have you ever had suicidal thoughts ?']

# Split data
X_train_sui, X_test_sui, y_train_sui, y_test_sui = train_test_split(
    X_suicidal, y_suicidal, test_size=TEST_RATIO, random_state=RANDOM_STATE
)

# Train model
suicidal_model = RandomForestClassifier(
    n_estimators=NUM_TREES,
    random_state=RANDOM_STATE
)
suicidal_model.fit(X_train_sui, y_train_sui)

# Evaluate
y_pred_sui = suicidal_model.predict(X_test_sui)
accuracy_sui = accuracy_score(y_test_sui, y_pred_sui)

print(f"\n   Suicidal Thoughts Model Performance:")
print(f"   Accuracy: {accuracy_sui * 100:.2f}%")
print(f"\n   Confusion Matrix:")
print(f"   {confusion_matrix(y_test_sui, y_pred_sui)}")
print(f"\n   Classification Report:")
print(classification_report(y_test_sui, y_pred_sui, target_names=['No', 'Yes']))

# Save model
with open('suicidal_model.pkl', 'wb') as f:
    pickle.dump(suicidal_model, f)
print("\n   ✓ Saved suicidal_model.pkl")

# ============================================================================
# Save Feature Information and Encodings
# ============================================================================
print("\n[5/6] Saving model metadata...")

model_info = {
    'depression_features': depression_features,
    'suicidal_features': suicidal_features,
    'encodings': encodings,
    'feature_order': depression_features,  # Both models use same features
    'depression_accuracy': accuracy_dep,
    'suicidal_accuracy': accuracy_sui
}

with open('model_info.pkl', 'wb') as f:
    pickle.dump(model_info, f)
print("   ✓ Saved model_info.pkl")

# ============================================================================
# Test Predictions
# ============================================================================
print("\n[6/6] Testing model predictions...")
print("-" * 60)

# Test sample: moderate risk profile
test_sample = pd.DataFrame([{
    'Gender': 1,  # Female
    'Age': 20,
    'Academic Pressure': 3.0,
    'Study Satisfaction': 3.0,
    'Sleep Duration': 2,  # 5-6 hours
    'Dietary Habits': 2,  # Moderate
    'Study Hours': 6,
    'Financial Stress': 3,
    'Family History of Mental Illness': 0  # No
}])

dep_pred = depression_model.predict(test_sample)[0]
dep_prob = depression_model.predict_proba(test_sample)[0]

sui_pred = suicidal_model.predict(test_sample)[0]
sui_prob = suicidal_model.predict_proba(test_sample)[0]

print(f"\n   Test Sample (Moderate Risk Profile):")
print(f"   - Female, Age 20, Academic Pressure 3/5")
print(f"   - Sleep 5-6 hours, Moderate diet, 6 study hours")
print(f"   - Financial Stress 3/5, No family history")
print(f"\n   Predictions:")
print(f"   Depression: {'Yes' if dep_pred == 1 else 'No'}")
print(f"     → No Depression: {dep_prob[0]:.2%}")
print(f"     → Depression: {dep_prob[1]:.2%}")
print(f"\n   Suicidal Thoughts: {'Yes' if sui_pred == 1 else 'No'}")
print(f"     → No: {sui_prob[0]:.2%}")
print(f"     → Yes: {sui_prob[1]:.2%}")

print("\n" + "=" * 60)
print("Training Complete! ✓")
print("=" * 60)
print("\nGenerated files:")
print("  • depression_model.pkl")
print("  • suicidal_model.pkl")
print("  • model_info.pkl")
print("\nModels are ready for integration into web applications.")

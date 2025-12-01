import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import sys
import os

sys.path.insert(1, '../../data')

from configs import data_dir, test_ratio, num_trees


print("=" * 60)
print("Training Depression Prediction Model")
print("=" * 60)

# Prepare data --------------------------------------------------------------------------
# Load the data into a DataFrame
print("\n[1/5] Loading dataset...")
df = pd.read_csv(data_dir)
print(f"   ✓ Loaded {len(df)} records")

# Convert categorical feature data into numerical data using label encoding
print("\n[2/5] Encoding categorical features...")
df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
df['Sleep Duration'] = df['Sleep Duration'].map({
    'Less than 5 hours': 1, 
    '5-6 hours': 2, 
    '7-8 hours': 3, 
    'More than 8 hours': 4
})
df['Dietary Habits'] = df['Dietary Habits'].map({'Unhealthy': 1, 'Moderate': 2, 'Healthy': 3})
df['Have you ever had suicidal thoughts ?'] = df['Have you ever had suicidal thoughts ?'].map({'No': 0, 'Yes': 1})
df['Family History of Mental Illness'] = df['Family History of Mental Illness'].map({'No': 0, 'Yes': 1})
df['Depression'] = df['Depression'].map({'No': 0, 'Yes': 1})
print("   ✓ Encoding complete")

# Features: All columns EXCEPT 'Depression' (target) and 'Suicidal Thoughts' (another target)
# We want to predict depression WITHOUT using suicidal thoughts as a feature
print("\n[3/5] Preparing features and target...")
feature_columns = [
    'Gender', 'Age', 'Academic Pressure', 'Study Satisfaction',
    'Sleep Duration', 'Dietary Habits', 'Study Hours',
    'Financial Stress', 'Family History of Mental Illness'
]

X = df[feature_columns]
y = df['Depression']
print(f"   ✓ Features: {len(feature_columns)} columns")
print(f"   ✓ Target: Depression")

# Split the data into test and train sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=42)
print(f"   ✓ Train set: {len(X_train)} samples")
print(f"   ✓ Test set: {len(X_test)} samples")

# Build the model-------------------------------------------------------------------------
print("\n[4/5] Training Random Forest model...")
model = RandomForestClassifier(n_estimators=num_trees, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("   ✓ Model trained")

# Evaluate the model----------------------------------------------------------------------
print("\n[5/5] Evaluating model performance...")
# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'\n   Accuracy: {accuracy * 100:.2f}%')

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print(f'\n   Confusion Matrix:')
print(f'   {conf_matrix}')

# Other statistics: precision, f1, etc
print(f'\n   Classification Report:')
print(classification_report(y_test, y_pred, target_names=['No Depression', 'Depression']))

# Save the model--------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Saving model...")
model_filename = 'depression_model.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump(model, f)
print(f"✓ Model saved as '{model_filename}'")

# Save feature information
model_info = {
    'feature_columns': feature_columns,
    'accuracy': accuracy,
    'model_type': 'depression'
}
with open('depression_model_info.pkl', 'wb') as f:
    pickle.dump(model_info, f)
print(f"✓ Model info saved as 'depression_model_info.pkl'")

print("=" * 60)
print("Depression model training complete!")
print("=" * 60)

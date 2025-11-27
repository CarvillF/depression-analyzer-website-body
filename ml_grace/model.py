import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from configs import data_dir, test_ratio, num_trees, sample

# Prepare data --------------------------------------------------------------------------
# Load the data into a DataFrame
df = pd.read_csv(data_dir)

# Convert categorical feature data into numerical data using label encoding
df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
df['Sleep Duration'] = df['Sleep Duration'].map({'Less than 5 hours': 1, '5-6 hours': 2, '7-8 hours': 3, 'More than 8 hours': 4})
df['Dietary Habits'] = df['Dietary Habits'].map({'Unhealthy': 1, 'Moderate': 2, 'Healthy': 3})
df['Have you ever had suicidal thoughts ?'] = df['Have you ever had suicidal thoughts ?'].map({'No': 0, 'Yes': 1})
df['Family History of Mental Illness'] = df['Family History of Mental Illness'].map({'No': 0, 'Yes': 1})

# Features will be stored in x (gender, age, etc)
# Target stored in y (depression categorization)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Split the data into test and train sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio)


# Build the model-------------------------------------------------------------------------
model = RandomForestClassifier(n_estimators=num_trees)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


# Evaluate the model----------------------------------------------------------------------
# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print(f'Confusion matrix:\n{conf_matrix}')

# Other statistics: precision, f1, etc
print(classification_report(y_test, y_pred))


# Use the model on a sample----------------------------------------------------------------
print(f'Prediction of depression: {model.predict(sample)[0]}')
print(f'Probability of no depression: {model.predict_proba(sample)[0][0]:.2f}')
print(f'Probability of depression: {model.predict_proba(sample)[0][1]:.2f}')
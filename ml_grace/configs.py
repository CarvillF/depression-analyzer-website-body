'''
Contains configuration information for easy access and updating
'''

import pandas as pd

data_dir = 'depression-analyzer-website-body/ml_grace/Depression Student Dataset.csv'
test_ratio = 0.3
num_trees = 1000

sample = pd.DataFrame([{
    'Gender': 1,
    'Age': 19,
    'Academic Pressure': 2.0,
    'Study Satisfaction': 3.0,
    'Sleep Duration': 4,
    'Dietary Habits': 3,
    'Have you ever had suicidal thoughts ?': 0,
    'Study Hours': 8,
    'Financial Stress': 1,
    'Family History of Mental Illness': 0
}])
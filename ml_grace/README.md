# ML Grace - Machine Learning Models

This directory contains the machine learning models for predicting depression and suicidal risk in students.

## Model Training Scripts

### Individual Model Training

**Depression Model:**
```bash
python depression_model.py
```
- Trains a Random Forest classifier for depression prediction
- Outputs: `depression_model.pkl`, `depression_model_info.pkl`
- Accuracy: ~82%

**Suicidal Risk Model:**
```bash
python suicidal_risk_model.py
```
- Trains a Random Forest classifier for suicidal thoughts prediction
- Outputs: `suicidal_model.pkl`, `suicidal_model_info.pkl`
- Accuracy: ~50% (harder prediction task)

### Train Both Models at Once

```bash
python train_all_models.py
```

This convenience script trains both models sequentially.

## Configuration

Edit `configs.py` to adjust:
- `data_dir`: Path to the dataset CSV file
- `test_ratio`: Train/test split ratio (default: 0.3)
- `num_trees`: Number of trees in Random Forest (default: 1000)

## Model Usage

The `model_utils.py` module provides functions for using the trained models:

```python
from model_utils import predict_both

# Get predictions for both depression and suicidal risk
results = predict_both(
    gender="Female",
    age=22,
    academic_pressure=3,
    study_satisfaction=4,
    sleep_duration="7-8 hours",
    dietary_habits="Healthy",
    study_hours=6,
    financial_stress=2,
    family_history="No"
)

# Results contain:
# - depression_prediction: 0 or 1
# - depression_probability: 0.0 to 1.0
# - suicidal_prediction: 0 or 1
# - suicidal_probability: 0.0 to 1.0
```

## Testing

Run the integration tests:
```bash
python test_integration.py
```

This tests the models with three different risk profiles (low, moderate, high).

## Files

- `depression_model.py` - Script to train depression prediction model
- `suicidal_risk_model.py` - Script to train suicidal risk prediction model
- `train_all_models.py` - Convenience script to train both models
- `model_utils.py` - Utility functions for loading and using models
- `configs.py` - Configuration parameters
- `test_integration.py` - Integration tests
- `Depression Student Dataset.csv` - Training data (502 records)

### Generated Model Files

After training, these files are created:
- `depression_model.pkl` - Trained depression model
- `depression_model_info.pkl` - Depression model metadata
- `suicidal_model.pkl` - Trained suicidal risk model
- `suicidal_model_info.pkl` - Suicidal risk model metadata

## Features

Both models use the same 9 input features:
1. Gender (Male=0, Female=1)
2. Age (18-34)
3. Academic Pressure (1-5)
4. Study Satisfaction (1-5)
5. Sleep Duration (1=<5h, 2=5-6h, 3=7-8h, 4=>8h)
6. Dietary Habits (1=Unhealthy, 2=Moderate, 3=Healthy)
7. Study Hours (0-12)
8. Financial Stress (1-5)
9. Family History of Mental Illness (No=0, Yes=1)

## Integration with Web Applications

The models are integrated into:
- `website_carlos/mvpVer/app.py` (Gradio interface)
- `website_carlos/targetVer/app.py` (Streamlit interface)

Both applications automatically load and use the trained models for predictions.

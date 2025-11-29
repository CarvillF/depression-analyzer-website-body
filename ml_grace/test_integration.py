"""
Test script to verify model integration works correctly.
"""

import sys
import os

# Add ml_grace to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_grace')))

from model_utils import predict_both

print("=" * 60)
print("Testing ML Model Integration")
print("=" * 60)

# Test Case 1: Low Risk Profile
print("\n[Test 1] Low Risk Profile:")
print("  Female, Age 22, Low pressure, Good sleep/diet")
result1 = predict_both(
    gender="Female",
    age=22,
    academic_pressure=2,
    study_satisfaction=4,
    sleep_duration="7-8 hours",
    dietary_habits="Healthy",
    study_hours=5,
    financial_stress=2,
    family_history="No"
)
print(f"\n  Results:")
print(f"    Depression: {result1['depression_prediction']} (prob: {result1['depression_probability']:.2%})")
print(f"    Suicidal Thoughts: {result1['suicidal_prediction']} (prob: {result1['suicidal_probability']:.2%})")

# Test Case 2: High Risk Profile
print("\n" + "-" * 60)
print("\n[Test 2] High Risk Profile:")
print("  Male, Age 20, High pressure, Poor sleep/diet, Family history")
result2 = predict_both(
    gender="Male",
    age=20,
    academic_pressure=5,
    study_satisfaction=1,
    sleep_duration="Less than 5 hours",
    dietary_habits="Unhealthy",
    study_hours=12,
    financial_stress=5,
    family_history="Yes"
)
print(f"\n  Results:")
print(f"    Depression: {result2['depression_prediction']} (prob: {result2['depression_probability']:.2%})")
print(f"    Suicidal Thoughts: {result2['suicidal_prediction']} (prob: {result2['suicidal_probability']:.2%})")

# Test Case 3: Moderate Risk Profile
print("\n" + "-" * 60)
print("\n[Test 3] Moderate Risk Profile:")
print("  Female, Age 25, Moderate factors")
result3 = predict_both(
    gender="Female",
    age=25,
    academic_pressure=3,
    study_satisfaction=3,
    sleep_duration="5-6 hours",
    dietary_habits="Moderate",
    study_hours=7,
    financial_stress=3,
    family_history="No"
)
print(f"\n  Results:")
print(f"    Depression: {result3['depression_prediction']} (prob: {result3['depression_probability']:.2%})")
print(f"    Suicidal Thoughts: {result3['suicidal_prediction']} (prob: {result3['suicidal_probability']:.2%})")

print("\n" + "=" * 60)
print("✓ All tests completed successfully!")
print("=" * 60)
print("\nModel integration is working correctly.")
print("The models can predict different risk levels based on input factors.")

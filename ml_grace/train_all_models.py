"""
Convenience script to train both models at once.
Run this script to retrain both the depression and suicidal risk models.
"""

import subprocess
import sys

print("=" * 70)
print("Training Both ML Models")
print("=" * 70)

# Train depression model
print("\n[1/2] Training Depression Model...")
print("-" * 70)
result1 = subprocess.run([sys.executable, "depression_model.py"], capture_output=False)

if result1.returncode != 0:
    print("\n❌ Error training depression model")
    sys.exit(1)

# Train suicidal risk model
print("\n[2/2] Training Suicidal Risk Model...")
print("-" * 70)
result2 = subprocess.run([sys.executable, "suicidal_risk_model.py"], capture_output=False)

if result2.returncode != 0:
    print("\n❌ Error training suicidal risk model")
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ Both models trained successfully!")
print("=" * 70)
print("\nGenerated files:")
print("  • depression_model.pkl")
print("  • depression_model_info.pkl")
print("  • suicidal_model.pkl")
print("  • suicidal_model_info.pkl")
print("\nModels are ready for use in web applications.")

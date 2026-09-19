import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Load the dataset (make sure the file name is correct)
df = pd.read_csv("sample_logs.csv")  # Corrected file name

# Simple feature engineering (you can expand this later)
X = df[['Hours_Ran', 'Error_Code']]
y = df['Error_Code']  # Assuming the Error_Code is used as label for failure cause

# Split for training (optional here since it's small data)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple classifier (Random Forest)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Ensure the 'model/' directory exists
os.makedirs("model", exist_ok=True)

# Save the trained model
joblib.dump(clf, "model/failure_cause_model.pkl")

print("✅ Model trained and saved as model/failure_cause_model.pkl")

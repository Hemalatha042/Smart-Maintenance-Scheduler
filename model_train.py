import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load the dataset
df = pd.read_csv("data/sample_logs.csv")

# Select features and target
X = df[['Hours_Ran', 'Error_Code']]
y = df['Failure']

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

# Make sure 'model/' directory exists
os.makedirs("model", exist_ok=True)

# Save the trained model
joblib.dump(model, "model/maintenance_model.pkl")

print("✅ Model trained and saved to model/maintenance_model.pkl")

# failure_cause_classifier.py

import pandas as pd
import joblib

# Load the model
model = joblib.load("model/failure_cause_model.pkl")

def classify_failure_cause(df):
    # Select only the features used during training
    X = df[['Hours_Ran', 'Error_Code']]
    
    # Predict failure causes
    predictions = model.predict(X)

    # Add predictions to DataFrame
    df['Failure_Cause'] = predictions
    return df

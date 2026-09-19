# maintenance_predictor.py

def predict_maintenance_hours(df):
    # Simple dummy prediction logic: assume machine fails at 1000 hours
    df['Predicted_Hours_Before_Breakdown'] = df['Hours_Ran'].apply(lambda x: 1000 - x)
    return df

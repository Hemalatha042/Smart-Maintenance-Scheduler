import joblib

def load_failure_model():
    return joblib.load("model/maintenance_model.pkl")

def predict_failures(df):
    model = load_failure_model()
    features = df[['Hours_Ran', 'Error_Code']]  # Adjust based on your training
    df['Maintenance_Required'] = model.predict(features)
    return df

def load_cause_model():
    return joblib.load("model/cause_classifier.pkl")

def classify_failure_cause(failure_df):
    model = load_cause_model()
    features = failure_df[['Error_Code']]  # Modify to match training
    return model.predict(features)

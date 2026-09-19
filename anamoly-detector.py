from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df):
    numeric_df = df.select_dtypes(include='number')

    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(numeric_df)

    df["Anomaly"] = model.predict(numeric_df)
    df["Anomaly"] = df["Anomaly"].replace({-1: "Yes", 1: "No"})
    return df

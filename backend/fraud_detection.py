import pandas as pd
from sklearn.ensemble import IsolationForest

def detect():
    df = pd.read_csv("data/transactions.csv")
    model = IsolationForest(contamination=0.07, random_state=42)
    df["anomaly"] = model.fit_predict(df[["amount"]])
    df["risk_score"] = (-model.decision_function(df[["amount"]])) * 100
    return df[df["anomaly"] == -1]

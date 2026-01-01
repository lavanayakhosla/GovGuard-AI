import shap
import pandas as pd
from sklearn.ensemble import IsolationForest

def explain():
    df = pd.read_csv("data/transactions.csv")
    model = IsolationForest()
    model.fit(df[["amount"]])
    explainer = shap.Explainer(model.predict, df[["amount"]])
    values = explainer(df[["amount"]])
    return values.values[:10].tolist()

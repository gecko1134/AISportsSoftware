import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("⚠️ Equipment Failure Predictor")

    uploaded = st.file_uploader("Upload equipment_maintenance.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        import datetime
        np.random.seed(42)
        df = pd.DataFrame({
            "equipment_id": [f"EQ_{i}" for i in range(1, 101)],
            "age_years": np.random.randint(1, 10, 100),
            "hours_used": np.random.randint(50, 1000, 100),
            "last_repair_days": np.random.randint(30, 300, 100),
            "failures_last_year": np.random.randint(0, 3, 100),
            "failed": np.random.choice([0, 1], 100, p=[0.8, 0.2])
        })

    st.subheader("📋 Equipment Maintenance Data")
    st.dataframe(df.head())

    X = df[["age_years", "hours_used", "last_repair_days", "failures_last_year"]]
    y = df["failed"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Failure Risk Classification Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["risk_score"] = model.predict_proba(X)[:, 1]
    high_risk = df[df["risk_score"] > 0.6]

    st.subheader("⚠️ High-Risk Equipment")
    st.dataframe(high_risk[["equipment_id", "risk_score"]].sort_values("risk_score", ascending=False))
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🙌 Volunteer Engagement Predictor")

    uploaded = st.file_uploader("Upload volunteer_shifts.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "volunteer_id": [f"V{i}" for i in range(100)],
            "shifts_last_90": np.random.randint(1, 10, 100),
            "attendance_rate": np.random.uniform(0.6, 1.0, 100).round(2),
            "satisfaction_score": np.random.uniform(3.0, 5.0, 100).round(1),
            "retained": np.random.choice([0, 1], 100, p=[0.3, 0.7])
        })

    st.subheader("📋 Volunteer Shift History")
    st.dataframe(df.head())

    X = df[["shifts_last_90", "attendance_rate", "satisfaction_score"]]
    y = df["retained"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Engagement Retention Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["retention_risk_score"] = 1 - model.predict_proba(X)[:, 1]
    flagged = df[df["retention_risk_score"] > 0.5]

    st.subheader("🚩 High-Risk Volunteers")
    st.dataframe(flagged[["volunteer_id", "retention_risk_score"]].sort_values("retention_risk_score", ascending=False))
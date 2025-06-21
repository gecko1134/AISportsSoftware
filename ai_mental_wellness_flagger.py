import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🧠 AI Mental Wellness Flagger")

    uploaded = st.file_uploader("Upload member_behavior.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "avg_sessions_week": np.random.uniform(0.5, 5.0, 100),
            "feedback_score": np.random.uniform(2.5, 5.0, 100),
            "days_since_last_visit": np.random.randint(1, 60, 100),
            "flagged_wellness": np.random.choice([0, 1], 100, p=[0.8, 0.2])
        })

    st.subheader("📋 Member Behavioral Data")
    st.dataframe(df.head())

    X = df[["avg_sessions_week", "feedback_score", "days_since_last_visit"]]
    y = df["flagged_wellness"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Wellness Risk Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["wellness_risk"] = model.predict_proba(X)[:, 1]
    flagged = df[df["wellness_risk"] > 0.6]

    st.subheader("🚩 Flagged for Wellness Check")
    st.dataframe(flagged[["member_id", "wellness_risk"]].sort_values("wellness_risk", ascending=False))
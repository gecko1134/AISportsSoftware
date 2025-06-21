import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🦵 Injury Risk Predictor")

    uploaded = st.file_uploader("Upload training_load.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "weekly_sessions": np.random.randint(1, 10, 100),
            "avg_intensity": np.random.uniform(0.5, 1.5, 100),
            "days_rest": np.random.randint(0, 5, 100),
            "previous_injury": np.random.choice([0, 1], 100),
            "injury_flag": np.random.choice([0, 1], 100, p=[0.85, 0.15])
        })

    st.subheader("📋 Member Training Load")
    st.dataframe(df.head())

    X = df[["weekly_sessions", "avg_intensity", "days_rest", "previous_injury"]]
    y = df["injury_flag"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    df["injury_risk"] = model.predict_proba(X)[:, 1]

    st.subheader("🚨 High-Risk Members for Injury")
    st.dataframe(df[df["injury_risk"] > 0.5][["member_id", "injury_risk"]].sort_values("injury_risk", ascending=False))

    st.subheader("📊 Classification Report")
    report = classification_report(y_test, model.predict(X_test), output_dict=True)
    st.json(report)
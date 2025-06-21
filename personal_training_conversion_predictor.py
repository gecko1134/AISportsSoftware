import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("💪 Personal Training Conversion Predictor")

    uploaded = st.file_uploader("Upload training_interest.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "avg_weekly_visits": np.random.uniform(1, 7, 100).round(1),
            "inquired_about_training": np.random.choice([0, 1], 100, p=[0.7, 0.3]),
            "goal_focus": np.random.choice(["Weight Loss", "Strength", "Endurance"], 100),
            "converted": np.random.choice([0, 1], 100, p=[0.8, 0.2])
        })

    st.subheader("📋 Member Training Interest")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    df["goal_code"] = df["goal_focus"].astype("category").cat.codes
    X = df[["tier_code", "avg_weekly_visits", "inquired_about_training", "goal_code"]]
    y = df["converted"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Conversion Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["conversion_score"] = model.predict_proba(X)[:, 1]
    st.subheader("🎯 Target Members for PT Promotion")
    st.dataframe(df[["member_id", "conversion_score"]].sort_values("conversion_score", ascending=False).head(10))
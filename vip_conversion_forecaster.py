import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("💎 VIP Conversion Forecaster")

    uploaded = st.file_uploader("Upload member_behavior.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "monthly_visits": np.random.randint(1, 30, 100),
            "avg_spend": np.random.randint(20, 500, 100),
            "referrals": np.random.randint(0, 5, 100),
            "converted_to_vip": np.random.choice([0, 1], 100, p=[0.85, 0.15])
        })

    st.subheader("📋 Member Behavior Data")
    st.dataframe(df.head())

    X = df[["monthly_visits", "avg_spend", "referrals"]]
    y = df["converted_to_vip"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    df["vip_conversion_score"] = model.predict_proba(X)[:, 1]

    st.subheader("🎯 Top Upgrade Candidates")
    st.dataframe(df.sort_values("vip_conversion_score", ascending=False)[["member_id", "vip_conversion_score"]].head(10))

    st.subheader("📊 Classification Report")
    report = classification_report(y_test, model.predict(X_test), output_dict=True)
    st.json(report)
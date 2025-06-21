import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("👥 Member Lifecycle Stage Classifier")

    uploaded = st.file_uploader("Upload member_engagement_history.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(60)],
            "days_since_join": np.random.randint(1, 720, 60),
            "avg_visits_last_30d": np.random.randint(0, 15, 60),
            "last_feedback_score": np.random.uniform(2.5, 5.0, 60).round(1)
        })

    def classify(row):
        if row["days_since_join"] < 30:
            return "🆕 Onboarding"
        elif row["avg_visits_last_30d"] >= 8 and row["last_feedback_score"] > 4:
            return "✅ Active"
        elif row["avg_visits_last_30d"] <= 2:
            return "⚠️ At Risk"
        else:
            return "↘️ Declining"

    df["lifecycle_stage"] = df.apply(classify, axis=1)

    st.subheader("📋 Member Lifecycle Prediction")
    st.dataframe(df[["member_id", "days_since_join", "avg_visits_last_30d", "last_feedback_score", "lifecycle_stage"]])
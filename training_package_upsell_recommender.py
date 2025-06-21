import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📦 Training Package Upsell Recommender")

    uploaded = st.file_uploader("Upload member_activity.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "avg_sessions_per_week": np.round(np.random.uniform(0.5, 5.0, 100), 1),
            "goal": np.random.choice(["Lose Weight", "Build Muscle", "General Fitness"], 100)
        })

    st.subheader("📋 Member Activity Data")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    df["score"] = (df["avg_sessions_per_week"] * 2) + df["tier_code"] * 3

    def suggest_package(row):
        if row["score"] > 10:
            return "Premium 1-on-1 Coaching"
        elif row["score"] > 6:
            return "Small Group Training"
        else:
            return "Digital Plan + App Access"

    df["recommended_upsell"] = df.apply(suggest_package, axis=1)

    st.subheader("💡 Suggested Upsell Packages")
    st.dataframe(df[["member_id", "tier", "avg_sessions_per_week", "goal", "recommended_upsell"]])
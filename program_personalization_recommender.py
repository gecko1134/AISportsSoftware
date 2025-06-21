import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎯 Program Personalization Recommender")

    uploaded = st.file_uploader("Upload member_history.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        goals = ["Weight Loss", "Strength", "Endurance"]
        programs = ["Yoga", "Bootcamp", "Cardio", "Weights", "Zumba"]
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "age": np.random.randint(18, 65, 100),
            "goal": np.random.choice(goals, 100),
            "sessions_last_month": np.random.randint(0, 12, 100)
        })

    st.subheader("📋 Member Profiles")
    st.dataframe(df.head())

    def recommend(row):
        if row["goal"] == "Weight Loss":
            return "Bootcamp" if row["sessions_last_month"] > 5 else "Zumba"
        elif row["goal"] == "Strength":
            return "Weights" if row["age"] > 30 else "Bootcamp"
        else:
            return "Cardio" if row["tier"] == "Silver" else "Yoga"

    df["recommended_program"] = df.apply(recommend, axis=1)

    st.subheader("🤖 Personalized Recommendations")
    st.dataframe(df[["member_id", "goal", "tier", "age", "sessions_last_month", "recommended_program"]])
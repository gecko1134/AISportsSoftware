import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🧠 Smart Session Suggester")

    uploaded = st.file_uploader("Upload member_sessions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "goal": np.random.choice(["Weight Loss", "Strength", "Wellness"], 100),
            "preferred_time": np.random.choice(["Morning", "Afternoon", "Evening"], 100),
            "past_top_session": np.random.choice(["HIIT", "Yoga", "Weights", "Spin"], 100)
        })

    st.subheader("📋 Member Session Profiles")
    st.dataframe(df.head())

    def recommend(row):
        if row["goal"] == "Weight Loss":
            return "HIIT" if row["preferred_time"] == "Morning" else "Cardio + Spin"
        elif row["goal"] == "Strength":
            return "Weights" if row["preferred_time"] != "Morning" else "Circuit Training"
        else:
            return "Yoga" if row["preferred_time"] == "Evening" else "Pilates + Stretch"

    df["recommended_session"] = df.apply(recommend, axis=1)

    st.subheader("✨ Personalized Session Suggestions")
    st.dataframe(df[["member_id", "goal", "preferred_time", "recommended_session"]])
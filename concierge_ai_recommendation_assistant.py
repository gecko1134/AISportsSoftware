import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🧠 Concierge AI Recommendation Assistant")

    uploaded = st.file_uploader("Upload member_profiles.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "goal": np.random.choice(["Weight Loss", "Strength", "Wellness"], 100),
            "sessions_last_30": np.random.randint(0, 15, 100),
            "preferred_time": np.random.choice(["Morning", "Evening", "Afternoon"], 100)
        })

    st.subheader("📋 Member Profile Data")
    st.dataframe(df.head())

    def suggest(row):
        if row["goal"] == "Weight Loss":
            rec = "Try HIIT or Bootcamp"
        elif row["goal"] == "Strength":
            rec = "Join Power Lifting or Circuit Training"
        else:
            rec = "Yoga + Wellness Workshop"

        if row["sessions_last_30"] < 5:
            rec += " + Personalized Starter Pack"

        if row["preferred_time"] == "Morning":
            rec += " at 7:00 AM"
        elif row["preferred_time"] == "Evening":
            rec += " after 6:00 PM"
        else:
            rec += " around 1:00 PM"

        return rec

    df["concierge_recommendation"] = df.apply(suggest, axis=1)
    st.subheader("✨ Concierge Recommendations")
    st.dataframe(df[["member_id", "tier", "goal", "preferred_time", "concierge_recommendation"]])
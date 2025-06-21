import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🖥️ Interactive Kiosk Recommendation Engine")

    uploaded = st.file_uploader("Upload kiosk_sessions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "location": np.random.choice(["Lobby", "Studio", "Cafe"], 100),
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "last_interaction": np.random.choice(["Fitness Tips", "Class Booking", "Event RSVP"], 100),
            "preferred_program": np.random.choice(["Yoga", "Bootcamp", "Cardio"], 100)
        })

    st.subheader("📋 Kiosk Session Data")
    st.dataframe(df.head())

    def recommend(row):
        if row["location"] == "Lobby" and row["tier"] == "VIP":
            return f"Early access to {row['preferred_program']} sessions"
        elif row["last_interaction"] == "Class Booking":
            return "Join our advanced Bootcamp next week"
        elif row["last_interaction"] == "Fitness Tips":
            return "Try our strength training series"
        else:
            return f"Check out a {row['preferred_program']} class nearby"

    df["recommendation"] = df.apply(recommend, axis=1)

    st.subheader("✨ Personalized Kiosk Suggestions")
    st.dataframe(df[["member_id", "location", "tier", "last_interaction", "recommendation"]])
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🕹️ Virtual Club Space Host")

    uploaded = st.file_uploader("Upload club_requests.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "club_name": np.random.choice(["Run Chat", "Yoga Talk", "Parent Circle", "Esports Night"], 30),
            "host": [f"U{i}" for i in range(30)],
            "type": np.random.choice(["Fitness", "Family", "Wellness", "Gaming"], 30),
            "expected_attendees": np.random.randint(10, 50, 30)
        })

    df["room"] = df["type"].map({
        "Fitness": "Zoom A",
        "Family": "Zoom B",
        "Wellness": "Zoom C",
        "Gaming": "Twitch Lobby"
    })

    st.subheader("🏠 Upcoming Club Sessions")
    st.dataframe(df[["club_name", "host", "type", "expected_attendees", "room"]])
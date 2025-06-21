import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🏃 Multi-Sport Participation Model")

    uploaded = st.file_uploader("Upload athlete_participation.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        users = [f"user_{i}" for i in range(1, 201)]
        sports = ["Soccer", "Basketball", "Swimming", "Tennis", "Lacrosse"]
        records = []
        for u in users:
            for s in np.random.choice(sports, size=np.random.randint(1, 4), replace=False):
                records.append({"user_id": u, "sport": s})
        df = pd.DataFrame(records)

    st.subheader("📋 Athlete Participation Data")
    st.dataframe(df.head())

    sport_count = df.groupby("user_id")["sport"].nunique().reset_index(name="sports_played")
    st.subheader("📊 Multisport Distribution")
    st.bar_chart(sport_count["sports_played"].value_counts().sort_index())

    multisport_users = sport_count[sport_count["sports_played"] > 1]
    st.metric("Multisport Athletes", len(multisport_users))
    st.metric("Total Athletes", sport_count.shape[0])
    st.metric("Crossover %", f"{100 * len(multisport_users) / sport_count.shape[0]:.1f}%")
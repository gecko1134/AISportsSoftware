import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🔐 AI Access Control Monitor")

    uploaded = st.file_uploader("Upload access_log.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        import numpy as np
        import random
        from datetime import datetime, timedelta

        np.random.seed(42)
        access_points = ["Main Gate", "Back Door", "Fitness Wing", "Locker Hall"]
        users = [f"user_{i}" for i in range(100)]
        now = datetime(2024, 6, 1)
        timestamps = [now - timedelta(hours=random.randint(0, 720)) for _ in range(500)]

        df = pd.DataFrame({
            "timestamp": timestamps,
            "user_id": np.random.choice(users, 500),
            "access_point": np.random.choice(access_points, 500),
            "result": np.random.choice(["Granted", "Denied"], 500, p=[0.95, 0.05])
        })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.dayofweek

    st.subheader("📋 Access Logs")
    st.dataframe(df.head())

    st.subheader("🔢 Entry Volume by Hour")
    hourly = df[df["result"] == "Granted"].groupby("hour").size()
    fig, ax = plt.subplots()
    hourly.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Entries")
    st.pyplot(fig)

    st.subheader("🚪 Access Point Heatmap")
    heatmap_data = pd.crosstab(df["access_point"], df["hour"])
    fig2, ax2 = plt.subplots()
    sns.heatmap(heatmap_data, annot=True, cmap="YlOrRd", fmt=".0f", ax=ax2)
    st.pyplot(fig2)

    st.subheader("🚨 Security Alert: Denied Access Attempts")
    st.dataframe(df[df["result"] == "Denied"])
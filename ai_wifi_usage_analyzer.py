import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("📶 AI WiFi Usage Analyzer")

    uploaded = st.file_uploader("Upload wifi_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        from datetime import datetime, timedelta
        np.random.seed(42)
        zones = ["Lobby", "Fitness", "Pool", "Cafe", "Gym"]
        timestamps = [datetime(2024, 1, 1) + timedelta(minutes=np.random.randint(0, 60*24*30)) for _ in range(1000)]
        df = pd.DataFrame({
            "timestamp": timestamps,
            "zone": np.random.choice(zones, 1000),
            "device_id": [f"dev_{i}" for i in np.random.randint(1, 500, 1000)]
        })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.dayofweek

    st.subheader("📋 WiFi Log Sample")
    st.dataframe(df.head())

    heatmap_data = df.groupby(["zone", "hour"])["device_id"].nunique().unstack().fillna(0)

    st.subheader("📈 Zone Activity Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Unique Devices by Zone & Hour")
    st.pyplot(fig)

    peak_zone = df["zone"].value_counts().idxmax()
    peak_hour = df["hour"].value_counts().idxmax()
    st.metric("Peak Zone", peak_zone)
    st.metric("Peak Hour", f"{peak_hour}:00")
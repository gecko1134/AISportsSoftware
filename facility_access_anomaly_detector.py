import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def run():
    st.title("🚨 Facility Access Anomaly Detector")

    uploaded = st.file_uploader("Upload access_log.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        users = [f"user_{i}" for i in range(1, 101)]
        access_points = ["Main", "Back", "Locker", "Gym"]
        timestamps = [datetime(2024, 1, 1) + timedelta(minutes=np.random.randint(0, 60*24*30)) for _ in range(1000)]
        df = pd.DataFrame({
            "timestamp": timestamps,
            "user_id": np.random.choice(users, 1000),
            "access_point": np.random.choice(access_points, 1000)
        })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.dayofweek

    st.subheader("📋 Access Log")
    st.dataframe(df.head())

    st.subheader("📈 Hourly Entry Volume")
    hourly = df.groupby("hour").size()
    st.bar_chart(hourly)

    # Flag entries outside 5 AM – 11 PM
    df["anomaly"] = df["hour"].apply(lambda h: h < 5 or h > 23)
    flagged = df[df["anomaly"]]

    st.subheader("🚩 Anomalous Access Entries")
    st.dataframe(flagged[["timestamp", "user_id", "access_point", "hour"]])
    st.metric("Total Anomalies", len(flagged))
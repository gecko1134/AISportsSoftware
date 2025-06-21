import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run():
    st.title("🚨 Real-Time Staff Alert Engine")

    uploaded = st.file_uploader("Upload facility_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        base = datetime(2024, 6, 1)
        df = pd.DataFrame({
            "timestamp": [base + timedelta(minutes=np.random.randint(0, 1440)) for _ in range(500)],
            "zone": np.random.choice(["Lobby", "Gym", "Pool", "Track"], 500),
            "people_count": np.random.randint(1, 60, 500),
            "incidents": np.random.choice([0, 1], 500, p=[0.95, 0.05])
        })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.subheader("📋 Facility Logs")
    st.dataframe(df.head())

    st.subheader("⚠️ Alerts")
    alerts = df[(df["people_count"] > 50) | (df["incidents"] > 0)]
    st.write("Triggered Alerts (Crowd > 50 or Incident)")
    st.dataframe(alerts)

    st.metric("Total Alerts", len(alerts))
    st.metric("Zones Monitored", df["zone"].nunique())
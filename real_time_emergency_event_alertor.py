import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run():
    st.title("🚨 Real-Time Emergency Event Alertor")

    uploaded = st.file_uploader("Upload incident_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        zones = ["Gym", "Lobby", "Pool", "Studio"]
        now = datetime(2024, 6, 1, 12)
        df = pd.DataFrame({
            "timestamp": [now - timedelta(minutes=np.random.randint(0, 120)) for _ in range(100)],
            "zone": np.random.choice(zones, 100),
            "event_type": np.random.choice(["fall", "fire", "medical", "crowding", "noise", "normal"], 100, p=[0.05, 0.03, 0.1, 0.1, 0.2, 0.52]),
            "severity": np.random.randint(1, 5, 100)
        })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.subheader("📋 Incident Log")
    st.dataframe(df.head())

    alert_keywords = ["fire", "fall", "medical"]
    active_alerts = df[df["event_type"].isin(alert_keywords) | (df["severity"] >= 4)]

    st.subheader("⚠️ Active Emergency Alerts")
    st.dataframe(active_alerts[["timestamp", "zone", "event_type", "severity"]])

    st.metric("Total Alerts", len(active_alerts))
    st.metric("Zones Affected", active_alerts["zone"].nunique())
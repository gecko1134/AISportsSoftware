import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🚨 Emergency Event Alert Predictor")

    uploaded = st.file_uploader("Upload event_schedule.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event": [f"Event {i}" for i in range(20)],
            "attendees": np.random.randint(50, 500, 20),
            "indoor": np.random.choice([1, 0], 20),
            "weather_alert": np.random.choice([0, 1], 20, p=[0.8, 0.2]),
            "maintenance_flag": np.random.choice([0, 1], 20, p=[0.9, 0.1])
        })

    df["risk_score"] = df["attendees"] * 0.01 + df["weather_alert"] * 2 + df["maintenance_flag"] * 3
    df["alert_level"] = pd.cut(df["risk_score"], bins=[0, 2, 4, 6, 10], labels=["Low", "Moderate", "High", "Critical"])

    st.subheader("🔍 Event Risk Overview")
    st.dataframe(df[["event", "attendees", "weather_alert", "maintenance_flag", "risk_score", "alert_level"]])
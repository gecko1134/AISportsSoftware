import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("💰 Event Overrun Cost Predictor")

    uploaded = st.file_uploader("Upload event_bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_name": [f"Event {i}" for i in range(30)],
            "expected_hours": np.random.randint(1, 5, 30),
            "actual_hours": np.random.randint(1, 6, 30),
            "expected_cost": np.random.randint(300, 1000, 30),
            "actual_cost": np.random.randint(300, 1200, 30)
        })

    df["time_overrun_hr"] = df["actual_hours"] - df["expected_hours"]
    df["cost_overrun_usd"] = df["actual_cost"] - df["expected_cost"]
    df["flagged"] = (df["time_overrun_hr"] > 0) | (df["cost_overrun_usd"] > 0)

    st.subheader("📋 Event Overrun Summary")
    st.dataframe(df)

    st.metric("⚠️ Overrun Events", df["flagged"].sum())
    st.metric("💸 Total Overrun ($)", df["cost_overrun_usd"].sum())
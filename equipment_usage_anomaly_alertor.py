import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🔍 Equipment Usage Anomaly Alertor")

    uploaded = st.file_uploader("Upload equipment_activity.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "equipment_id": [f"E{i}" for i in range(100)],
            "zone": np.random.choice(["Gym", "Track", "Studio"], 100),
            "avg_daily_usage_min": np.random.normal(60, 15, 100).round(),
            "std_dev_usage": np.random.uniform(5, 20, 100).round(1)
        })

    st.subheader("📋 Equipment Usage Logs")
    st.dataframe(df.head())

    # Anomaly flag: either very high or low compared to standard deviation
    df["z_score"] = (df["avg_daily_usage_min"] - df["avg_daily_usage_min"].mean()) / df["std_dev_usage"]
    df["is_anomaly"] = df["z_score"].abs() > 2

    anomalies = df[df["is_anomaly"]]
    st.subheader("🚨 Flagged Anomalous Equipment")
    st.dataframe(anomalies[["equipment_id", "zone", "avg_daily_usage_min", "std_dev_usage", "z_score"]])

    st.metric("Total Anomalies", len(anomalies))
    st.metric("Total Monitored", len(df))

    fig, ax = plt.subplots()
    ax.hist(df["avg_daily_usage_min"], bins=15, color="coral")
    ax.set_title("Distribution of Daily Equipment Usage (min)")
    ax.set_xlabel("Usage Minutes")
    st.pyplot(fig)
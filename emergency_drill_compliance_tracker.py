import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🧯 Emergency Drill Compliance Tracker")

    uploaded = st.file_uploader("Upload drill_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "staff_id": [f"S{i}" for i in range(100)],
            "role": np.random.choice(["Trainer", "Cleaner", "Front Desk"], 100),
            "responded": np.random.choice([1, 0], 100, p=[0.85, 0.15]),
            "response_time_sec": np.random.randint(10, 300, 100)
        })

    st.subheader("📋 Drill Participation Logs")
    st.dataframe(df.head())

    avg_time = df[df["responded"] == 1]["response_time_sec"].mean()
    st.metric("Avg Response Time", f"{avg_time:.1f} sec")

    noncompliant = df[(df["responded"] == 0) | (df["response_time_sec"] > 180)]
    st.subheader("🚨 Noncompliant Staff")
    st.dataframe(noncompliant[["staff_id", "role", "responded", "response_time_sec"]])
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🕒 Staff Overtime Risk Monitor")

    uploaded = st.file_uploader("Upload staff_schedules.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "staff_id": [f"S{i}" for i in range(100)],
            "role": np.random.choice(["Trainer", "Cleaner", "Front Desk"], 100),
            "weekly_hours": np.random.randint(30, 60, 100),
            "shifts": np.random.randint(3, 7, 100),
            "weeks_active": np.random.randint(1, 52, 100)
        })

    st.subheader("📋 Weekly Staff Workload")
    st.dataframe(df.head())

    df["risk_flag"] = df["weekly_hours"] > 45
    risk_df = df[df["risk_flag"]]

    st.subheader("⚠️ High Overtime Risk Staff")
    st.dataframe(risk_df[["staff_id", "role", "weekly_hours", "shifts", "weeks_active"]])

    st.metric("Total Staff", len(df))
    st.metric("Overtime Risk", f"{len(risk_df)} staff ({100 * len(risk_df) / len(df):.1f}%)")
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📋 Staff Performance Review Tool")

    uploaded = st.file_uploader("Upload staff_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "staff_id": [f"S{i}" for i in range(30)],
            "attendance_rate": np.random.uniform(0.85, 1.0, 30).round(2),
            "on_time_rate": np.random.uniform(0.7, 1.0, 30).round(2),
            "feedback_score": np.random.uniform(3.0, 5.0, 30).round(2)
        })

    df["performance_score"] = ((df["attendance_rate"] * 0.4 + df["on_time_rate"] * 0.3 + (df["feedback_score"] / 5) * 0.3) * 100).round(1)

    st.subheader("🌟 Staff Performance Summary")
    st.dataframe(df.sort_values("performance_score", ascending=False))
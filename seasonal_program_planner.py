import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📅 Seasonal Program Planner")

    uploaded = st.file_uploader("Upload historical_program_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "program_name": np.random.choice(["Youth Fit", "Spring Shred", "Summer Yoga", "Winter Strong"], 40),
            "season": np.random.choice(["Spring", "Summer", "Fall", "Winter"], 40),
            "attendance_avg": np.random.randint(20, 100, 40),
            "feedback_avg": np.random.uniform(3.5, 5.0, 40).round(1)
        })

    summary = df.groupby("season").agg({
        "attendance_avg": "mean",
        "feedback_avg": "mean"
    }).round(1)

    st.subheader("📊 Seasonal Program Trends")
    st.dataframe(summary)

    top = df[df["attendance_avg"] > 75]
    st.subheader("🌟 High-Impact Programs to Repeat")
    st.dataframe(top)
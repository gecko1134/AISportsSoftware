import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("📊 Program Retention Analyzer")

    uploaded = st.file_uploader("Upload program_enrollments.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        import numpy as np
        import random
        from datetime import datetime, timedelta

        np.random.seed(42)
        programs = ["Youth Soccer", "Pickleball Intro", "Senior Fitness", "Basketball League"]
        start_dates = [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(200)]
        retention_days = [random.randint(30, 400) for _ in range(200)]

        df = pd.DataFrame({
            "user_id": [f"user_{i}" for i in range(200)],
            "program": np.random.choice(programs, 200),
            "start_date": start_dates,
            "retention_days": retention_days
        })

    st.subheader("📋 Enrollment Data")
    st.dataframe(df.head())

    avg_retention = df.groupby("program")["retention_days"].mean().sort_values(ascending=False)
    st.subheader("📈 Average Retention Days per Program")
    st.dataframe(avg_retention.reset_index())

    fig, ax = plt.subplots()
    avg_retention.plot(kind="bar", color="seagreen", ax=ax)
    ax.set_ylabel("Average Days")
    ax.set_title("Program Retention")
    st.pyplot(fig)
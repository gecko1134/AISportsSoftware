import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("💼 Corporate Booking Block Optimizer")

    uploaded = st.file_uploader("Upload corporate_requests.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "company": ["CorpX", "TechCo", "Wellness Group"],
            "attendees": [60, 35, 100],
            "preferred_day": ["Tuesday", "Friday", "Wednesday"],
            "preferred_start": [9, 13, 10],
            "duration_hr": [3, 2, 4],
            "rate_per_hr": [150, 180, 200]
        })

    st.subheader("📋 Corporate Booking Requests")
    st.dataframe(df)

    df["end_time"] = df["preferred_start"] + df["duration_hr"]
    df["estimated_invoice"] = df["duration_hr"] * df["rate_per_hr"]

    st.subheader("📈 Booking Block Summary")
    st.dataframe(df[["company", "preferred_day", "preferred_start", "end_time", "estimated_invoice"]])
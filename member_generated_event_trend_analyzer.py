import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📆 Member-Generated Event Trend Analyzer")

    uploaded = st.file_uploader("Upload user_created_events.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_name": np.random.choice(["Dodgeball Night", "Yoga Jam", "Family Spin", "Bootcamp", "Stretch & Chat"], 50),
            "category": np.random.choice(["Fitness", "Social", "Kids", "Wellness"], 50),
            "date": pd.date_range("2024-01-01", periods=50, freq="3D"),
            "attendance": np.random.randint(5, 80, 50),
            "feedback_avg": np.random.uniform(3.0, 5.0, 50).round(1)
        })

    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    trend = df.groupby(["month", "category"])["attendance"].mean().unstack().fillna(0)

    st.subheader("📊 Monthly Attendance Trend by Category")
    st.dataframe(trend.round(1))

    st.line_chart(trend)
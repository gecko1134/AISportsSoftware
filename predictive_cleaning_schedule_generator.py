import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🧼 Predictive Cleaning Schedule Generator")

    uploaded = st.file_uploader("Upload zone_usage.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "zone": np.random.choice(["Court", "Turf", "Studio", "Locker Room", "Cafe"], 50),
            "avg_hourly_visits": np.random.randint(5, 50, 50),
            "days_since_cleaned": np.random.randint(0, 7, 50),
            "rain_factor": np.random.choice([0, 1], 50, p=[0.8, 0.2])
        })

    df["cleaning_score"] = (df["avg_hourly_visits"] * 0.3 + df["days_since_cleaned"] * 2 + df["rain_factor"] * 5).round(1)
    df["priority"] = pd.cut(df["cleaning_score"], bins=[-1, 6, 12, 20, 40], labels=["Low", "Moderate", "High", "Critical"])

    st.subheader("🧾 Suggested Cleaning Priorities")
    st.dataframe(df.sort_values("cleaning_score", ascending=False))
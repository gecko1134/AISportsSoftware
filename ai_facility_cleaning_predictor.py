import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🧽 Facility Cleaning Predictor")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Booking Data")
    st.dataframe(df.head())

    df["hour"] = df["time"].str.extract(r"(\d+):").astype(int)
    df["weekday"] = pd.to_datetime(df["date"]).dt.dayofweek

    usage = df.groupby("facility_id").size().reset_index(name="booking_count")
    usage["last_cleaned_days_ago"] = np.random.randint(1, 14, len(usage))
    usage["cleaning_priority"] = (usage["booking_count"] * 0.6 + usage["last_cleaned_days_ago"] * 0.4).round(2)

    st.subheader("🧼 Cleaning Priority Scores")
    st.dataframe(usage.sort_values("cleaning_priority", ascending=False))

    fig, ax = plt.subplots()
    usage.plot(x="facility_id", y="cleaning_priority", kind="bar", ax=ax, legend=False, color="darkred")
    ax.set_ylabel("Priority Score")
    ax.set_title("Predicted Cleaning Need by Facility")
    st.pyplot(fig)
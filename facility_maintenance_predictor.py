import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("🛠️ Facility Maintenance Predictor")

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
    usage["usage_hours"] = usage["booking_count"] * 1  # assume 1 hour per booking
    usage["maintenance_score"] = usage["usage_hours"] / usage["usage_hours"].max()
    usage["maintenance_score"] = usage["maintenance_score"].round(2)

    st.subheader("🔧 Maintenance Risk by Facility")
    st.dataframe(usage.sort_values("maintenance_score", ascending=False))

    fig, ax = plt.subplots()
    ax.bar(usage["facility_id"].astype(str), usage["maintenance_score"], color="salmon")
    ax.set_ylabel("Relative Maintenance Score (0-1)")
    ax.set_xlabel("Facility ID")
    ax.set_title("Maintenance Risk Forecast")
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🏐 Court Utilization Predictor")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Booking Data")
    st.dataframe(df.head())

    df["hour"] = df["time"].str.extract(r"(\d+):").astype(int)
    df["weekday"] = pd.to_datetime(df["date"]).dt.dayofweek
    df["court_id"] = df["facility_id"].astype("category")

    grouped = df.groupby(["court_id", "hour", "weekday"]).size().reset_index(name="bookings")

    X = grouped[["hour", "weekday"]]
    y = grouped["bookings"]

    model = GradientBoostingRegressor()
    model.fit(X, y)
    grouped["predicted_demand"] = model.predict(X)

    st.subheader("📈 Predicted Demand by Hour/Weekday")
    fig, ax = plt.subplots()
    for court in grouped["court_id"].unique():
        subset = grouped[grouped["court_id"] == court]
        ax.plot(subset["hour"], subset["predicted_demand"], label=f"Court {court}")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Predicted Demand")
    ax.set_title("Court Demand Forecast")
    ax.legend()
    st.pyplot(fig)
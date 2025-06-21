import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("💸 Dynamic Discount Optimizer")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Booking Data")
    st.dataframe(df.head())

    df["hour"] = df["time"].str.extract(r"(\d+):").astype(int)
    df["weekday"] = pd.to_datetime(df["date"]).dt.dayofweek
    df["slot"] = df["hour"].astype(str) + "-" + df["weekday"].astype(str)

    demand = df["slot"].value_counts().reset_index()
    demand.columns = ["slot", "bookings"]
    demand[["hour", "weekday"]] = demand["slot"].str.split("-", expand=True).astype(int)

    # Calculate discounts: lower bookings = higher discount
    max_b = demand["bookings"].max()
    demand["discount_pct"] = 100 - (demand["bookings"] / max_b * 100)
    demand["discount_pct"] = demand["discount_pct"].clip(lower=5).round(0)

    st.subheader("📉 Suggested Discounts by Time Slot")
    st.dataframe(demand.sort_values("discount_pct", ascending=False)[["hour", "weekday", "discount_pct"]])

    fig, ax = plt.subplots()
    ax.scatter(demand["hour"], demand["discount_pct"], c=demand["weekday"], cmap="viridis", s=80)
    ax.set_title("Discount Recommendations by Hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Discount %")
    st.pyplot(fig)
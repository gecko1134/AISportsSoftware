import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("🕓 Waitlist Optimizer")

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

    slot_counts = df["slot"].value_counts().reset_index()
    slot_counts.columns = ["slot", "count"]
    slot_counts["hour"] = slot_counts["slot"].str.split("-").str[0].astype(int)
    slot_counts["weekday"] = slot_counts["slot"].str.split("-").str[1].astype(int)

    pivot = slot_counts.pivot("hour", "weekday", "count").fillna(0)

    st.subheader("📊 Occupancy Heatmap (Busy = Higher Count)")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax)
    ax.set_title("Booking Saturation: Hour vs Weekday")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Hour")
    st.pyplot(fig)

    st.subheader("🔍 Suggested Waitlist Openings")
    low_demand = slot_counts[slot_counts["count"] < slot_counts["count"].quantile(0.4)]
    st.dataframe(low_demand.sort_values("count").head(10))
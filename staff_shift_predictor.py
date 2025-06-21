import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("👥 Staff Shift Predictor")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Booking Data")
    st.dataframe(df.head())

    df["hour"] = df["time"].str.extract(r"(\d+):").astype(int)
    df["weekday"] = pd.to_datetime(df["date"]).dt.dayofweek
    df["sport_type"] = df["sport_type"].astype("category")

    pivot = df.pivot_table(index="hour", columns="sport_type", values="member_id", aggfunc="count").fillna(0)

    st.subheader("📈 Bookings Heatmap by Hour x Sport")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

    st.subheader("🔁 Suggested Staffing Levels")
    load = pivot.sum(axis=1)
    staff_df = pd.DataFrame({
        "Hour": load.index,
        "Bookings": load.values,
        "Suggested Staff": np.ceil(load.values / 8).astype(int)
    })
    st.dataframe(staff_df)
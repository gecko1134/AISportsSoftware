import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🔥 Facility Usage Heatmap")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Bookings Data")
    st.dataframe(df.head())

    df["hour"] = df["time"].str.extract(r"(\d+):").astype(int)
    df["weekday"] = pd.to_datetime(df["date"]).dt.dayofweek

    pivot = df.pivot_table(index="hour", columns="weekday", values="member_id", aggfunc="count").fillna(0)

    st.subheader("📊 Heatmap of Usage")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt=".0f", linewidths=.5, ax=ax)
    ax.set_title("Facility Usage by Hour and Weekday")
    ax.set_xlabel("Weekday (0=Mon)")
    ax.set_ylabel("Hour")
    st.pyplot(fig)
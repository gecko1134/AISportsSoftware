import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("🏢 Multi-Facility Usage Model")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Booking Data")
    st.dataframe(df.head())

    df["hour"] = df["time"].str.extract(r"(\d+):").astype(int)
    df["weekday"] = pd.to_datetime(df["date"]).dt.dayofweek

    usage = df.groupby(["facility_id", "hour"]).size().reset_index(name="bookings")

    pivot = usage.pivot(index="hour", columns="facility_id", values="bookings").fillna(0)
    st.subheader("📈 Hourly Load by Facility")
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind="line", ax=ax)
    ax.set_ylabel("Bookings")
    ax.set_title("Hourly Facility Usage")
    st.pyplot(fig)

    st.subheader("📊 Total Facility Load")
    totals = df["facility_id"].value_counts().sort_index()
    st.bar_chart(totals)
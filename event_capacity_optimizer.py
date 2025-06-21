import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def run():
    st.title("🏟️ Event Capacity Optimizer")

    uploaded = st.file_uploader("Upload events.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("events.csv")

    st.subheader("📋 Event Data")
    st.dataframe(df.head())

    threshold = st.slider("Venue Capacity Limit", 50, 1000, 300)

    df["overbooked"] = df["expected_attendance"] > threshold
    df["underbooked"] = df["expected_attendance"] < threshold * 0.5

    over = df[df["overbooked"]]
    under = df[df["underbooked"]]

    st.subheader("⚠️ Overbooked Events")
    st.dataframe(over[["event_id", "date", "sport", "expected_attendance"]])

    st.subheader("📉 Underbooked Events")
    st.dataframe(under[["event_id", "date", "sport", "expected_attendance"]])

    fig, ax = plt.subplots()
    ax.hist(df["expected_attendance"], bins=20, color="purple")
    ax.axvline(threshold, color="red", linestyle="--", label="Capacity Limit")
    ax.axvline(threshold * 0.5, color="blue", linestyle="--", label="50% Threshold")
    ax.set_title("Expected Attendance Distribution")
    ax.legend()
    st.pyplot(fig)
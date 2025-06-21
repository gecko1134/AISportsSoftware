import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📈 Member Growth Trend Analyzer")

    uploaded = st.file_uploader("Upload member_trend_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "month": pd.date_range("2023-01-01", periods=24, freq="M"),
            "new_members": np.random.randint(30, 150, 24),
            "churned_members": np.random.randint(10, 100, 24)
        })

    st.subheader("📋 Monthly Membership Changes")
    st.dataframe(df.head())

    df["net_change"] = df["new_members"] - df["churned_members"]
    df["total_members"] = df["net_change"].cumsum() + 1000

    st.subheader("📊 Membership Growth Overview")
    fig, ax = plt.subplots()
    ax.plot(df["month"], df["total_members"], label="Total Members")
    ax.plot(df["month"], df["net_change"], label="Net Change", linestyle="--")
    ax.set_ylabel("Members")
    ax.set_title("Membership Trends Over Time")
    ax.legend()
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📊 Competitor Program Benchmark Analyzer")

    uploaded = st.file_uploader("Upload program_benchmarks.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "program": ["Yoga", "Bootcamp", "Swim", "Cardio"] * 2,
            "provider": ["Your Club"] * 4 + ["Competitor A", "Competitor B", "Competitor A", "Competitor B"],
            "price": [60, 80, 50, 55, 65, 90, 45, 60],
            "duration_weeks": [6, 8, 5, 4, 6, 8, 5, 4]
        })

    st.subheader("📋 Benchmark Data")
    st.dataframe(df)

    pivot = df.pivot(index="program", columns="provider", values="price")
    st.subheader("💵 Price Comparison")
    st.dataframe(pivot)

    fig, ax = plt.subplots()
    for provider in df["provider"].unique():
        subset = df[df["provider"] == provider]
        ax.plot(subset["program"], subset["price"], marker="o", label=provider)
    ax.set_ylabel("Price ($)")
    ax.set_title("Program Pricing by Provider")
    ax.legend()
    st.pyplot(fig)
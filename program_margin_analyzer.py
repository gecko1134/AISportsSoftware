import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📊 Program Margin Analyzer")

    uploaded = st.file_uploader("Upload program_financials.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "program": np.random.choice(["Yoga", "Bootcamp", "Swim", "Weights"], 100),
            "revenue": np.random.randint(1000, 5000, 100),
            "instructor_cost": np.random.randint(400, 1500, 100),
            "facility_cost": np.random.randint(300, 1000, 100),
            "marketing_cost": np.random.randint(100, 800, 100)
        })

    df["total_cost"] = df["instructor_cost"] + df["facility_cost"] + df["marketing_cost"]
    df["margin"] = ((df["revenue"] - df["total_cost"]) / df["revenue"]).round(2)

    st.subheader("📋 Margin Summary")
    st.dataframe(df[["program", "revenue", "total_cost", "margin"]])

    avg_margin = df.groupby("program")["margin"].mean().sort_values(ascending=False)

    st.subheader("💵 Avg Margin by Program")
    st.bar_chart(avg_margin)

    low_margin = df[df["margin"] < 0.1]
    st.subheader("🚨 Low-Margin Programs (<10%)")
    st.dataframe(low_margin[["program", "margin", "revenue", "total_cost"]])
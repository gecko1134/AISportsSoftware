import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📈 Dynamic Membership Revenue Tracker")

    uploaded = st.file_uploader("Upload membership_revenue.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        months = pd.date_range("2023-01-01", periods=12, freq="M").strftime("%b %Y")
        df = pd.DataFrame({
            "month": np.tile(months, 3),
            "tier": np.repeat(["Silver", "Gold", "VIP"], 12),
            "members": np.random.randint(100, 600, 36),
            "monthly_fee": np.repeat([30, 50, 80], 12)
        })

    df["revenue"] = df["members"] * df["monthly_fee"]
    summary = df.groupby(["month", "tier"])["revenue"].sum().reset_index()

    st.subheader("📊 Revenue by Tier and Month")
    st.dataframe(summary)

    pivot = summary.pivot(index="month", columns="tier", values="revenue").fillna(0)
    st.line_chart(pivot)

    st.subheader("📍 Total Revenue Forecast")
    st.metric("Projected Monthly Avg", f"${int(df['revenue'].mean()):,}")
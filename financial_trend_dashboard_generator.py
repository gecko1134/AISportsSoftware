import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📈 Financial Trend Dashboard Generator")

    uploaded = st.file_uploader("Upload financial_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        months = pd.date_range(start="2024-01-01", periods=12, freq="M")
        df = pd.DataFrame({
            "month": np.tile(months, 3),
            "category": np.repeat(["Yoga", "Bootcamp", "Swim"], 12),
            "revenue": np.random.randint(5000, 15000, 36),
            "cost": np.random.randint(3000, 10000, 36)
        })

    df["margin"] = df["revenue"] - df["cost"]
    df["month"] = pd.to_datetime(df["month"])

    st.subheader("📊 Monthly Financial Summary")
    st.dataframe(df.head())

    category = st.selectbox("Select Category", sorted(df["category"].unique()))
    df_cat = df[df["category"] == category]

    st.subheader(f"📈 Trend for {category}")
    fig, ax = plt.subplots()
    ax.plot(df_cat["month"], df_cat["revenue"], label="Revenue", marker="o")
    ax.plot(df_cat["month"], df_cat["cost"], label="Cost", marker="x")
    ax.plot(df_cat["month"], df_cat["margin"], label="Margin", marker="s")
    ax.set_ylabel("Amount ($)")
    ax.set_title(f"{category} - Monthly Financial Trend")
    ax.legend()
    st.pyplot(fig)
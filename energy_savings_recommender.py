import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("💡 Energy Savings Recommender")

    uploaded = st.file_uploader("Upload energy_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "zone": np.random.choice(["Gym", "Pool", "Studio", "Track"], 200),
            "hour": np.random.randint(6, 22, 200),
            "kwh": np.random.uniform(1.5, 10.0, 200).round(2),
            "is_peak": np.random.choice([0, 1], 200, p=[0.7, 0.3])
        })

    st.subheader("📋 Energy Usage Logs")
    st.dataframe(df.head())

    savings = df.groupby("zone")["kwh"].sum().sort_values(ascending=False)
    st.subheader("⚡ Total Usage by Zone")
    st.bar_chart(savings)

    df["savings_if_shifted"] = df.apply(lambda row: row["kwh"] * 0.15 if row["is_peak"] else 0, axis=1)
    zone_savings = df.groupby("zone")["savings_if_shifted"].sum().sort_values(ascending=False)

    st.subheader("💸 Potential Savings by Shifting Peak Usage")
    st.dataframe(zone_savings.round(2).reset_index().rename(columns={"savings_if_shifted": "kWh Saved"}))

    fig, ax = plt.subplots()
    zone_savings.plot(kind="bar", ax=ax, color="green")
    ax.set_ylabel("kWh Saved")
    ax.set_title("Recommended Peak Usage Reductions")
    st.pyplot(fig)
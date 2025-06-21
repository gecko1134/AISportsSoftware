import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🌿 Carbon Footprint Estimator")

    uploaded = st.file_uploader("Upload utility_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "zone": np.random.choice(["Gym", "Pool", "Track", "Lobby"], 100),
            "month": np.random.choice(pd.date_range("2024-01-01", periods=6, freq="M"), 100),
            "kwh": np.random.uniform(500, 3000, 100),
            "natural_gas_therms": np.random.uniform(20, 150, 100),
            "water_gal": np.random.uniform(1000, 5000, 100)
        })

    st.subheader("📋 Utility Data")
    st.dataframe(df.head())

    # Conversion factors (approx)
    CO2_PER_KWH = 0.0007  # metric tons
    CO2_PER_THERM = 0.0053
    CO2_PER_GAL_WATER = 0.0000015

    df["carbon_kg"] = (
        df["kwh"] * CO2_PER_KWH * 1000 +
        df["natural_gas_therms"] * CO2_PER_THERM * 1000 +
        df["water_gal"] * CO2_PER_GAL_WATER * 1000
    )

    total = df.groupby("zone")["carbon_kg"].sum()
    st.subheader("🌎 Estimated CO2 Emissions (kg) by Zone")
    st.bar_chart(total)

    fig, ax = plt.subplots()
    df.groupby("month")["carbon_kg"].sum().plot(kind="line", marker="o", ax=ax)
    ax.set_title("Monthly Carbon Emissions")
    ax.set_ylabel("kg CO₂e")
    st.pyplot(fig)

    st.metric("Total Estimated Emissions", f"{df['carbon_kg'].sum():,.0f} kg")
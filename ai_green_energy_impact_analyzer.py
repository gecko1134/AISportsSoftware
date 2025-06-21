import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🌱 AI Green Energy Impact Analyzer")

    uploaded = st.file_uploader("Upload green_energy_upgrades.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "upgrade_type": ["LED", "Solar Panels", "HVAC", "LED", "HVAC", "Solar Panels"],
            "months_since_install": np.random.randint(1, 36, 6),
            "monthly_kwh_saved": np.random.randint(200, 1500, 6),
            "upgrade_cost": np.random.randint(5000, 30000, 6)
        })

    st.subheader("📋 Upgrade Records")
    st.dataframe(df)

    df["total_kwh_saved"] = df["months_since_install"] * df["monthly_kwh_saved"]
    df["co2_kg_saved"] = df["total_kwh_saved"] * 0.7  # average 0.7kg CO2 saved per kWh
    df["cost_per_kg_co2"] = (df["upgrade_cost"] / df["co2_kg_saved"]).round(2)

    st.subheader("📈 Environmental Impact Summary")
    st.dataframe(df[["upgrade_type", "total_kwh_saved", "co2_kg_saved", "cost_per_kg_co2"]])

    fig, ax = plt.subplots()
    df.groupby("upgrade_type")["co2_kg_saved"].sum().plot(kind="bar", ax=ax, color="green")
    ax.set_ylabel("Total CO₂ Saved (kg)")
    ax.set_title("CO₂ Reduction by Upgrade Type")
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🧪 Digital Twin Usage Simulator")

    uploaded = st.file_uploader("Upload zone_parameters.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Lobby", "Court", "Track", "Turf", "Cafe"]
        df = pd.DataFrame({
            "zone": zones,
            "lighting_level": np.random.uniform(0.5, 1.5, len(zones)).round(2),
            "entry_flow": np.random.randint(10, 100, len(zones)),
            "zone_size": np.random.randint(300, 1500, len(zones))
        })

    st.subheader("📋 Zone Configuration Inputs")
    st.dataframe(df)

    df["simulated_usage"] = (df["entry_flow"] * df["lighting_level"] * df["zone_size"] / 1000).round()
    st.subheader("📈 Simulated Zone Usage Output")
    st.dataframe(df[["zone", "simulated_usage"]].sort_values("simulated_usage", ascending=False))

    fig, ax = plt.subplots()
    df.plot(x="zone", y="simulated_usage", kind="bar", ax=ax, color="mediumblue")
    ax.set_title("Digital Twin Simulated Usage (by Zone)")
    st.pyplot(fig)
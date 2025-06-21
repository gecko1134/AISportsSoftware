import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🌿 AI Environmental Control Optimizer")

    uploaded = st.file_uploader("Upload environmental_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Turf", "Court", "Lobby", "Locker Room", "Track", "Cafe"]
        df = pd.DataFrame({
            "zone": np.random.choice(zones, 300),
            "hour": np.random.randint(6, 22, 300),
            "occupancy": np.random.randint(5, 100, 300),
            "current_temp": np.random.uniform(65, 78, 300),
            "light_level": np.random.uniform(0.5, 1.5, 300)
        })

    st.subheader("📋 Environmental Logs")
    st.dataframe(df.head())

    def recommend_temp(row):
        return 72 if row["occupancy"] > 50 else 70

    def recommend_light(row):
        return 1.2 if row["hour"] < 8 or row["hour"] > 19 else 1.0

    df["recommended_temp"] = df.apply(recommend_temp, axis=1)
    df["recommended_light"] = df.apply(recommend_light, axis=1)

    st.subheader("⚙️ Optimized Environmental Settings")
    st.dataframe(df[["zone", "hour", "occupancy", "recommended_temp", "recommended_light"]])
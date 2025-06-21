import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("📐 AI Facility Zoning Optimizer")

    uploaded = st.file_uploader("Upload zone_usage.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "zone": ["Gym", "Studio", "Pool", "Track", "Lobby", "Locker", "Cafe"],
            "avg_hourly_traffic": np.random.randint(5, 80, 7),
            "capacity": [100, 40, 60, 80, 50, 30, 25]
        })

    st.subheader("📋 Zone Usage Data")
    st.dataframe(df)

    df["utilization_pct"] = (df["avg_hourly_traffic"] / df["capacity"]).round(2)
    df["reallocation_flag"] = df["utilization_pct"].apply(lambda x: "Overused" if x > 0.85 else ("Underused" if x < 0.3 else "Balanced"))

    st.subheader("📊 Utilization & Reallocation Suggestions")
    st.dataframe(df[["zone", "avg_hourly_traffic", "capacity", "utilization_pct", "reallocation_flag"]])

    fig, ax = plt.subplots()
    sns.barplot(x="zone", y="utilization_pct", data=df, hue="reallocation_flag", dodge=False, ax=ax)
    ax.set_title("Zone Utilization vs. Capacity")
    ax.axhline(0.85, color="red", linestyle="--", label="Overuse Threshold")
    ax.axhline(0.3, color="blue", linestyle="--", label="Underuse Threshold")
    ax.set_ylabel("Utilization %")
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🌐 Multi-Location Usage Comparator")

    uploaded = st.file_uploader("Upload location_usage.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        locations = ["North", "South", "East", "West", "Central"]
        df = pd.DataFrame({
            "location": np.random.choice(locations, 200),
            "checkins": np.random.randint(100, 5000, 200),
            "retention_pct": np.random.uniform(0.3, 0.95, 200).round(2),
            "revenue": np.random.randint(5000, 40000, 200),
            "capacity": np.random.randint(1000, 8000, 200)
        })

    st.subheader("📋 Facility Usage by Location")
    st.dataframe(df.head())

    agg = df.groupby("location").agg({
        "checkins": "mean",
        "retention_pct": "mean",
        "revenue": "mean",
        "capacity": "mean"
    }).round().sort_values("checkins", ascending=False)

    st.subheader("📊 Location Comparison Summary")
    st.dataframe(agg)

    fig, ax = plt.subplots()
    agg[["checkins", "revenue"]].plot(kind="bar", ax=ax)
    ax.set_ylabel("Avg Monthly")
    ax.set_title("Check-ins & Revenue by Location")
    st.pyplot(fig)
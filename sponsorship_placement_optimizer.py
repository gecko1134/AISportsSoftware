import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📢 Sponsorship Placement Optimizer")

    uploaded = st.file_uploader("Upload sponsor_exposure.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Turf A", "Court 1", "Lobby Screen", "Email Newsletter", "Event Banner"]
        sponsors = ["BrandX", "FitFuel", "HydroCo", "SpeedPro", "GlowWear"]
        df = pd.DataFrame({
            "placement": np.random.choice(zones, 100),
            "sponsor": np.random.choice(sponsors, 100),
            "impressions": np.random.randint(100, 5000, 100),
            "clicks": np.random.randint(5, 400, 100),
            "duration_days": np.random.randint(7, 60, 100)
        })

    st.subheader("📋 Sponsor Exposure Logs")
    st.dataframe(df.head())

    df["click_through_rate"] = (df["clicks"] / df["impressions"]).round(3)
    df["roi_score"] = (df["click_through_rate"] * df["impressions"]) / df["duration_days"]

    st.subheader("📈 Placement Effectiveness by Sponsor")
    summary = df.groupby("placement")[["impressions", "clicks", "roi_score"]].mean().sort_values("roi_score", ascending=False).round(2)
    st.dataframe(summary)

    fig, ax = plt.subplots()
    summary["roi_score"].plot(kind="bar", ax=ax, color="green")
    ax.set_title("ROI Score by Sponsorship Placement")
    ax.set_ylabel("ROI (Normalized)")
    st.pyplot(fig)
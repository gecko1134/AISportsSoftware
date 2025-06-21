import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🖼️ AI Virtual Banner Rotation Scheduler")

    uploaded = st.file_uploader("Upload banner_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        banners = ["BrandX", "HydroFuel", "GlowGear", "FitLife", "LocalBank"]
        df = pd.DataFrame({
            "banner": np.random.choice(banners, 100),
            "hour": np.random.randint(6, 22, 100),
            "impressions": np.random.randint(50, 800, 100)
        })

    st.subheader("📋 Banner Impression Logs")
    st.dataframe(df.head())

    summary = df.groupby(["banner", "hour"])["impressions"].sum().reset_index()
    rotation = summary.groupby("hour").apply(lambda x: x.sort_values("impressions", ascending=False).head(1)).reset_index(drop=True)

    st.subheader("📆 Optimal Rotation Schedule")
    st.dataframe(rotation.sort_values("hour"))

    fig = df.groupby("hour")["impressions"].sum().plot(kind="bar", title="Impressions by Hour", ylabel="Total Impressions")
    st.pyplot(fig.figure)
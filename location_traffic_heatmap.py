import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("📍 Location Traffic Heatmap")

    uploaded = st.file_uploader("Upload entry_exit_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Main Gate", "Court Entrance", "Turf Zone", "Track Gate", "Cafe"]
        df = pd.DataFrame({
            "zone": np.random.choice(zones, 300),
            "hour": np.random.randint(6, 22, 300)
        })

    st.subheader("📋 Entry/Exit Records")
    st.dataframe(df.head())

    heatmap_data = df.groupby(["zone", "hour"]).size().unstack().fillna(0)
    st.subheader("🔥 Hourly Foot Traffic Heatmap")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlOrBr", ax=ax)
    ax.set_title("Traffic Volume by Zone and Hour")
    st.pyplot(fig)
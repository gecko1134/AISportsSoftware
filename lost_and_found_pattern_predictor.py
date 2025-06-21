import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🧢 Lost and Found Pattern Predictor")

    uploaded = st.file_uploader("Upload lost_items.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Locker Room", "Turf A", "Court 1", "Lobby", "Cafe", "Track"]
        df = pd.DataFrame({
            "item": np.random.choice(["Phone", "Bottle", "Towel", "Keys", "Wallet"], 200),
            "zone": np.random.choice(zones, 200),
            "hour": np.random.randint(6, 22, 200)
        })

    st.subheader("📋 Lost Item Logs")
    st.dataframe(df.head())

    zone_counts = df["zone"].value_counts().reset_index()
    zone_counts.columns = ["zone", "lost_count"]

    st.subheader("📍 High-Risk Zones")
    st.dataframe(zone_counts)

    heatmap_data = df.groupby(["zone", "hour"]).size().unstack().fillna(0)
    st.subheader("🔥 Hour-by-Zone Lost Item Heatmap")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Reds", ax=ax)
    ax.set_title("Lost Item Incidents by Zone and Hour")
    st.pyplot(fig)
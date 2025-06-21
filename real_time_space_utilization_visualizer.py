import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("📊 Real-Time Space Utilization Visualizer")

    uploaded = st.file_uploader("Upload zone_activity_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Turf A", "Turf B", "Court 1", "Court 2", "Track"]
        df = pd.DataFrame({
            "zone": np.random.choice(zones, 200),
            "hour": np.random.randint(6, 22, 200),
            "usage_sqft": np.random.randint(200, 4000, 200)
        })

    st.subheader("📋 Zone Activity Logs")
    st.dataframe(df.head())

    pivot = df.groupby(["zone", "hour"])["usage_sqft"].sum().unstack().fillna(0)
    st.subheader("🟧 Hour-by-Zone Usage Heatmap")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    ax.set_title("Real-Time Square Foot Usage (by Hour)")
    st.pyplot(fig)

    busiest = pivot.max(axis=1).idxmax()
    quietest = pivot.min(axis=1).idxmin()
    st.metric("Busiest Zone (Max Hour)", busiest)
    st.metric("Quietest Zone", quietest)
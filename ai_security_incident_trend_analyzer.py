import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🛡️ AI Security Incident Trend Analyzer")

    uploaded = st.file_uploader("Upload incident_reports.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        zones = ["Lobby", "Turf", "Court 1", "Locker Room", "Cafe", "Parking Lot"]
        types = ["Theft", "Vandalism", "Medical", "Harassment", "Disruption"]
        df = pd.DataFrame({
            "zone": np.random.choice(zones, 300),
            "incident_type": np.random.choice(types, 300),
            "hour": np.random.randint(6, 23, 300),
            "weekday": np.random.randint(0, 7, 300)
        })

    st.subheader("📋 Incident Reports")
    st.dataframe(df.head())

    heatmap_data = df.groupby(["zone", "hour"]).size().unstack().fillna(0)
    st.subheader("🚨 Incident Density Heatmap (by Hour)")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Reds", ax=ax)
    ax.set_title("Incident Count by Zone & Hour")
    st.pyplot(fig)

    top_alerts = df["zone"].value_counts().head(5).reset_index()
    top_alerts.columns = ["zone", "total_incidents"]
    st.subheader("⚠️ Zones with Highest Incident Volume")
    st.dataframe(top_alerts)
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🚿 Real-Time Shower & Locker Demand Tracker")

    uploaded = st.file_uploader("Upload facility_checkins.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "zone": np.random.choice(["Shower", "Locker", "Pool", "Studio"], 300),
            "hour": np.random.randint(6, 22, 300),
            "checkins": np.random.randint(1, 20, 300)
        })

    st.subheader("📋 Check-in Records")
    st.dataframe(df.head())

    pivot = df.groupby(["zone", "hour"])["checkins"].sum().unstack().fillna(0)
    st.subheader("🔥 Hourly Demand Heatmap")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_title("Check-in Demand by Zone & Hour")
    st.pyplot(fig)

    peak_hours = pivot.T.idxmax().to_frame("Peak Hour").reset_index()
    st.subheader("🚨 Peak Hour Detection")
    st.dataframe(peak_hours)
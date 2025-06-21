import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🚗 Parking Lot Congestion Predictor")

    uploaded = st.file_uploader("Upload parking_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "day": np.random.randint(0, 7, 300),
            "hour": np.random.randint(6, 22, 300),
            "vehicle_count": np.random.randint(10, 200, 300)
        })

    st.subheader("📋 Parking Lot Logs")
    st.dataframe(df.head())

    heatmap_data = df.groupby(["day", "hour"])["vehicle_count"].mean().unstack().fillna(0)

    st.subheader("🔥 Hour-by-Day Parking Congestion Heatmap")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)
    ax.set_title("Avg Vehicle Count (by Day & Hour)")
    st.pyplot(fig)

    busiest = heatmap_data.max().idxmax(), heatmap_data.max().max()
    st.metric("Peak Hour", f"{busiest[0]}:00", f"{int(busiest[1])} cars")
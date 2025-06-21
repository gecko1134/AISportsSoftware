import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🚌 Public Transport Arrival Optimizer")

    uploaded = st.file_uploader("Upload transit_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "stop": np.random.choice(["Main", "North", "South", "East"], 500),
            "arrival_hour": np.random.randint(6, 22, 500),
            "count": np.random.randint(1, 20, 500)
        })

    st.subheader("📋 Transit Arrival Logs")
    st.dataframe(df.head())

    hour_avg = df.groupby("arrival_hour")["count"].sum()
    st.subheader("🕒 Transit Volume by Hour")
    st.bar_chart(hour_avg)

    best_windows = hour_avg.sort_values(ascending=False).head(5).index.tolist()
    st.subheader("📌 Suggested Class Start Times")
    st.write(f"Top 5 recommended hours based on transit volume: {best_windows}")

    fig, ax = plt.subplots()
    hour_avg.plot(kind="line", marker="o", ax=ax)
    ax.set_ylabel("Total Arrivals")
    ax.set_title("Transit Arrival Flow by Hour")
    st.pyplot(fig)
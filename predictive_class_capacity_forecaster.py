import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📊 Predictive Class Capacity Forecaster")

    uploaded = st.file_uploader("Upload class_signups.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "class_type": np.random.choice(["Spin", "HIIT", "Yoga", "Weights"], 100),
            "hour": np.random.choice(range(6, 22), 100),
            "day": np.random.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], 100),
            "signups": np.random.randint(5, 30, 100)
        })

    summary = df.groupby(["class_type", "hour"])["signups"].mean().unstack().fillna(0)
    st.subheader("📈 Average Signups by Class & Hour")
    st.dataframe(summary)

    fig, ax = plt.subplots(figsize=(10, 4))
    for ctype in summary.index:
        ax.plot(summary.columns, summary.loc[ctype], label=ctype)
    ax.set_ylabel("Avg Signups")
    ax.set_title("Demand Forecast by Hour")
    ax.legend()
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📺 AI Streaming Content Insight Tracker")

    uploaded = st.file_uploader("Upload streaming_sessions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "content_type": np.random.choice(["Workout", "Event", "Wellness", "Promo"], 200),
            "duration_minutes": np.random.randint(5, 60, 200),
            "avg_watch_time": np.random.uniform(2, 60, 200),
            "replays": np.random.randint(0, 20, 200)
        })

    st.subheader("📋 Streaming Session Logs")
    st.dataframe(df.head())

    df["completion_rate"] = (df["avg_watch_time"] / df["duration_minutes"]).clip(0, 1).round(2)

    summary = df.groupby("content_type").agg({
        "avg_watch_time": "mean",
        "completion_rate": "mean",
        "replays": "sum"
    }).round(2)

    st.subheader("📊 Streaming Insights by Content Type")
    st.dataframe(summary)

    fig, ax = plt.subplots()
    summary["completion_rate"].plot(kind="bar", ax=ax, color="skyblue", title="Completion Rate by Content Type")
    ax.set_ylabel("Avg Completion %")
    st.pyplot(fig)
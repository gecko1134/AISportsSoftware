import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📱 Social Media Post Performance Tracker")

    uploaded = st.file_uploader("Upload post_metrics.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "post_id": [f"P{i}" for i in range(40)],
            "type": np.random.choice(["Story", "Reel", "Image", "Carousel"], 40),
            "likes": np.random.randint(50, 500, 40),
            "shares": np.random.randint(10, 100, 40),
            "comments": np.random.randint(5, 50, 40),
            "signups_generated": np.random.randint(0, 20, 40)
        })

    df["engagement_score"] = (df["likes"] + df["shares"] * 2 + df["comments"] * 3).round(1)

    st.subheader("📊 Content Performance Table")
    st.dataframe(df.sort_values("engagement_score", ascending=False))

    st.subheader("📈 Avg Engagement by Type")
    avg_engagement = df.groupby("type")["engagement_score"].mean().sort_values(ascending=False)
    st.bar_chart(avg_engagement)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📢 Sponsor Impact Tracker")

    st.write("Track sponsor exposure based on event reach and media impressions.")

    uploaded = st.file_uploader("Upload sponsor_events.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        # Generate synthetic data
        np.random.seed(42)
        sponsors = [f"Sponsor {i}" for i in range(1, 11)]
        df = pd.DataFrame({
            "sponsor": np.random.choice(sponsors, 100),
            "event_reach": np.random.randint(100, 2000, 100),
            "media_mentions": np.random.randint(0, 50, 100)
        })

    st.subheader("📋 Exposure Data")
    st.dataframe(df.head())

    df["impact_score"] = df["event_reach"] * 0.7 + df["media_mentions"] * 30
    summary = df.groupby("sponsor")["impact_score"].sum().sort_values(ascending=False).reset_index()

    st.subheader("📈 Sponsor Impact Scores")
    st.dataframe(summary)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(summary["sponsor"], summary["impact_score"], color="teal")
    ax.set_ylabel("Impact Score")
    ax.set_title("Total Exposure per Sponsor")
    plt.xticks(rotation=45)
    st.pyplot(fig)
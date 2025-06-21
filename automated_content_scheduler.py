import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📆 Automated Content Scheduler")

    uploaded = st.file_uploader("Upload content_library.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "content_id": [f"C{i}" for i in range(20)],
            "channel": np.random.choice(["Email", "App", "Kiosk"], 20),
            "content_type": np.random.choice(["Promo", "Reminder", "Education"], 20),
            "engagement_score": np.random.uniform(0.2, 1.0, 20).round(2),
            "target_segment": np.random.choice(["Youth", "Adults", "Seniors"], 20)
        })

    st.subheader("📋 Content Library")
    st.dataframe(df)

    def recommend_time(row):
        if row["channel"] == "Email":
            return "10:00 AM" if row["engagement_score"] > 0.6 else "2:00 PM"
        elif row["channel"] == "App":
            return "6:00 PM" if row["target_segment"] == "Adults" else "8:00 AM"
        else:
            return "8:30 AM" if row["content_type"] == "Promo" else "1:00 PM"

    df["recommended_time"] = df.apply(recommend_time, axis=1)

    st.subheader("⏰ Publishing Schedule")
    st.dataframe(df[["content_id", "channel", "content_type", "target_segment", "recommended_time"]])

    fig, ax = plt.subplots()
    df["recommended_time"].value_counts().plot(kind="bar", ax=ax, color="navy")
    ax.set_title("Distribution of Scheduled Times")
    st.pyplot(fig)
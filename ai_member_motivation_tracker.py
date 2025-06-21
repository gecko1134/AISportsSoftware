import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎯 AI Member Motivation Tracker")

    uploaded = st.file_uploader("Upload member_engagement.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(60)],
            "visits_last_30d": np.random.randint(0, 12, 60),
            "app_opens": np.random.randint(0, 20, 60),
            "feedback_score": np.random.uniform(2.0, 5.0, 60).round(1)
        })

    df["motivation_score"] = (df["visits_last_30d"] * 0.5 + df["app_opens"] * 0.3 + df["feedback_score"] * 2).round(1)
    df["flag"] = df["motivation_score"].apply(lambda x: "✅ Engaged" if x > 20 else "⚠️ Nudge Needed")

    st.subheader("📊 Member Motivation Index")
    st.dataframe(df.sort_values("motivation_score"))
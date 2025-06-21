import streamlit as st
import pandas as pd
import numpy as np
from textblob import TextBlob

def run():
    st.title("🧘 AI Mental Wellness Check-In Engine")

    uploaded = st.file_uploader("Upload wellness_checkins.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "sessions_last_30_days": np.random.randint(0, 12, 100),
            "feedback_text": np.random.choice([
                "Feeling great about my progress.",
                "Just okay, not very motivated lately.",
                "Staff is friendly and supportive.",
                "Not sleeping well, feeling off.",
                "Loving the sessions!",
                "Considering a break."
            ], 100)
        })

    st.subheader("📋 Member Wellness Check-In Logs")
    st.dataframe(df.head())

    df["sentiment"] = df["feedback_text"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["flag_for_checkin"] = ((df["sentiment"] < 0.1) | (df["sessions_last_30_days"] < 3))

    st.subheader("🚩 Members Needing Check-In")
    st.dataframe(df[df["flag_for_checkin"]][["member_id", "sessions_last_30_days", "sentiment", "feedback_text"]])
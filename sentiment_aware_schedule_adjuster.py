import streamlit as st
import pandas as pd
from textblob import TextBlob
import numpy as np

def run():
    st.title("😊 Sentiment-Aware Schedule Adjuster")

    uploaded = st.file_uploader("Upload schedule_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "session_id": [f"S{i}" for i in range(40)],
            "class_type": np.random.choice(["Yoga", "Spin", "HIIT"], 40),
            "hour": np.random.choice(range(6, 22), 40),
            "feedback_text": np.random.choice([
                "Loved the energy!", "Too early", "Room was cold", "Instructor was great", 
                "Felt rushed", "Would prefer afternoon", "Great flow", "Needs more music"
            ], 40)
        })

    df["sentiment"] = df["feedback_text"].apply(lambda x: round(TextBlob(x).sentiment.polarity, 2))
    df["suggestion"] = df.apply(
        lambda x: "🕓 Try moving to later hour" if x["sentiment"] < 0 and x["hour"] < 10 else (
            "📣 Keep this time slot" if x["sentiment"] > 0.3 else "🔄 Review setup"
        ), axis=1
    )

    st.subheader("🗓️ Feedback-Driven Schedule Adjustments")
    st.dataframe(df[["session_id", "class_type", "hour", "sentiment", "suggestion"]])
import streamlit as st
import pandas as pd
from textblob import TextBlob
import numpy as np

def run():
    st.title("📝 AI Event Summary Writer")

    uploaded = st.file_uploader("Upload event_attendance_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_name": np.random.choice(["Spin Social", "Wellness Day", "Family Fit", "HIIT Throwdown"], 20),
            "attendees": np.random.randint(20, 100, 20),
            "feedback_text": np.random.choice([
                "Amazing energy and great music!",
                "Really needed more water stations.",
                "Perfect weekend vibe — loved it!",
                "Tough but satisfying workout.",
                "Could be better organized next time."
            ], 20)
        })

    summaries = []
    for event in df["event_name"].unique():
        entries = df[df["event_name"] == event]
        sentiment_avg = entries["feedback_text"].apply(lambda x: TextBlob(x).sentiment.polarity).mean()
        tone = "positive" if sentiment_avg > 0.2 else "mixed" if sentiment_avg > 0 else "critical"
        summaries.append({
            "event_name": event,
            "attendees": entries["attendees"].sum(),
            "tone": tone,
            "summary": f"{event} attracted {entries['attendees'].sum()} attendees with overall {tone} feedback tone. Highlights included: {entries['feedback_text'].iloc[0]}"
        })

    result = pd.DataFrame(summaries)
    st.subheader("📋 AI-Generated Event Summaries")
    st.dataframe(result)
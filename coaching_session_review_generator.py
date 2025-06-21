import streamlit as st
import pandas as pd
from textblob import TextBlob

def run():
    st.title("🧠 Coaching Session Review Generator")

    uploaded = st.file_uploader("Upload coach_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "session_id": [f"S{i}" for i in range(20)],
            "coach_notes": [
                "Great focus today, good pacing.",
                "Needs more warm-up, rushed early sets.",
                "Excellent teamwork and form.",
                "Low energy today, likely fatigue.",
                "Strong push on final round, good effort!"
            ] * 4
        })

    df["sentiment"] = df["coach_notes"].apply(lambda x: round(TextBlob(x).sentiment.polarity, 2))
    df["summary"] = df["coach_notes"].apply(lambda x: x.split(",")[0] + ".")

    st.subheader("📝 Session Summary & Sentiment")
    st.dataframe(df[["session_id", "summary", "sentiment"]])
import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

def run():
    st.title("🧠 Event Feedback Analyzer")

    uploaded = st.file_uploader("Upload event_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_id": [1, 2, 1, 3, 2, 3, 1],
            "comment": [
                "Loved the event, very organized!",
                "Too crowded and poorly managed.",
                "Amazing atmosphere and good staff.",
                "It was okay, but could be better.",
                "Great event overall, will return!",
                "Weather ruined the experience.",
                "Facilities were clean and helpful staff."
            ]
        })

    st.subheader("📋 Feedback Comments")
    st.dataframe(df)

    df["sentiment"] = df["comment"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["category"] = pd.cut(df["sentiment"], bins=[-1, -0.1, 0.1, 1], labels=["Negative", "Neutral", "Positive"])

    st.subheader("📊 Sentiment Summary")
    sentiment_counts = df["category"].value_counts().sort_index()
    st.bar_chart(sentiment_counts)

    st.subheader("📌 Top Positive Comments")
    st.write(df[df["category"] == "Positive"][["event_id", "comment"]])

    st.subheader("⚠️ Negative Feedback")
    st.write(df[df["category"] == "Negative"][["event_id", "comment"]])
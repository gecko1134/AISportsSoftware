import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

def run():
    st.title("📣 Social Media Sentiment Monitor")

    uploaded = st.file_uploader("Upload social_mentions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "platform": ["Twitter", "Instagram", "Facebook"] * 50,
            "mention": [
                "Great event today at the dome!",
                "Parking was really confusing.",
                "Loved the new turf layout.",
                "App keeps crashing at login.",
                "Staff was super friendly today!",
                "Court 2 needs cleaning urgently."
            ] * 25
        })

    st.subheader("📋 Social Mentions")
    st.dataframe(df.head())

    df["sentiment"] = df["mention"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["tone"] = df["sentiment"].apply(lambda x: "Positive" if x > 0.2 else ("Negative" if x < -0.1 else "Neutral"))

    sentiment_summary = df["tone"].value_counts().reset_index()
    sentiment_summary.columns = ["Sentiment", "Count"]
    st.subheader("📊 Sentiment Distribution")
    st.dataframe(sentiment_summary)

    fig, ax = plt.subplots()
    sentiment_summary.set_index("Sentiment").plot(kind="bar", ax=ax, legend=False, color="skyblue")
    ax.set_title("Public Sentiment from Social Mentions")
    st.pyplot(fig)
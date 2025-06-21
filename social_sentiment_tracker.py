import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

def run():
    st.title("📢 Social Sentiment Tracker")

    uploaded = st.file_uploader("Upload social_mentions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "platform": ["Twitter", "Facebook", "Instagram", "Twitter", "Instagram"],
            "mention": [
                "Love this new sports complex! So clean and friendly staff.",
                "Parking is always full, frustrating experience.",
                "Great events and fun for families.",
                "Not enough basketball courts during weekends.",
                "Awesome staff and great variety of programs!"
            ]
        })

    st.subheader("📋 Mentions Sample")
    st.dataframe(df)

    df["sentiment"] = df["mention"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["category"] = pd.cut(df["sentiment"], [-1, -0.1, 0.1, 1], labels=["Negative", "Neutral", "Positive"])

    st.subheader("📊 Sentiment Breakdown")
    sentiment_counts = df["category"].value_counts().sort_index()
    st.bar_chart(sentiment_counts)

    st.subheader("📌 Negative Mentions")
    st.write(df[df["category"] == "Negative"][["platform", "mention"]])
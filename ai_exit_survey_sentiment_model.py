import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

def run():
    st.title("📤 Exit Survey Sentiment Model")

    uploaded = st.file_uploader("Upload exit_surveys.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"MEM_{i}" for i in range(1, 11)],
            "exit_reason": [
                "Too expensive and not enough value",
                "Loved the programs but moved away",
                "Not satisfied with cleanliness",
                "Friendly staff but schedule didn't work",
                "Great experience overall, just relocating",
                "Limited options for my age group",
                "Excellent facility but parking was an issue",
                "Felt like it was too crowded",
                "Didn't feel welcomed by the team",
                "Happy with my time here, but job transfer"
            ]
        })

    st.subheader("📋 Exit Survey Comments")
    st.dataframe(df)

    df["sentiment"] = df["exit_reason"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["sentiment_category"] = pd.cut(df["sentiment"], bins=[-1, -0.1, 0.1, 1], labels=["Negative", "Neutral", "Positive"])

    st.subheader("📊 Sentiment Summary")
    sentiment_counts = df["sentiment_category"].value_counts().sort_index()
    st.bar_chart(sentiment_counts)

    st.subheader("🚨 Negative Feedback")
    st.write(df[df["sentiment_category"] == "Negative"][["member_id", "exit_reason"]])
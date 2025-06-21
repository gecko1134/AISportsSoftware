import streamlit as st
import pandas as pd
from textblob import TextBlob

def run():
    st.title("😊 AI Mood-Based Offer Recommender")

    uploaded = st.file_uploader("Upload recent_sentiment.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(10)],
            "recent_comment": [
                "Loving the new classes!",
                "Pretty good overall but could improve",
                "Feeling unmotivated lately",
                "Staff has been very helpful",
                "Not as clean as before",
                "Amazing energy in sessions!",
                "Worried about pricing changes",
                "Classes have been too crowded",
                "Everything is going well",
                "I miss my old trainer"
            ]
        })

    st.subheader("📋 Member Feedback")
    st.dataframe(df)

    df["sentiment"] = df["recent_comment"].apply(lambda x: TextBlob(x).sentiment.polarity)

    def recommend_offer(score):
        if score > 0.3:
            return "Loyalty Bonus Offer"
        elif score < -0.1:
            return "Free 1-Week Booster Pass"
        else:
            return "Check-In & Chat Follow-Up"

    df["recommended_offer"] = df["sentiment"].apply(recommend_offer)

    st.subheader("🎁 Offer Suggestions Based on Sentiment")
    st.dataframe(df[["member_id", "sentiment", "recommended_offer"]])
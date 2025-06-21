import streamlit as st
import pandas as pd
from textblob import TextBlob

def run():
    st.title("✉️ AI Program Feedback Response Generator")

    uploaded = st.file_uploader("Upload program_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(1, 6)],
            "program": ["Yoga", "Swim", "Basketball", "Fitness", "Yoga"],
            "feedback": [
                "Loved the class! Great instructor and music.",
                "Pool area was not very clean this time.",
                "Too many people in the class, hard to concentrate.",
                "The trainer was excellent and really motivating.",
                "Great session, but the room was a little too cold."
            ]
        })

    st.subheader("📋 Feedback Entries")
    st.dataframe(df)

    def generate_reply(row):
        sentiment = TextBlob(row["feedback"]).sentiment.polarity
        if sentiment > 0.2:
            return f"Hi {row['member_id']}, we're thrilled you enjoyed the {row['program']} class! Thanks for your feedback."
        elif sentiment < -0.2:
            return f"Hi {row['member_id']}, thanks for your honesty about the {row['program']} session. We're reviewing your concerns closely."
        else:
            return f"Hi {row['member_id']}, we appreciate your feedback on the {row['program']} class and will use it to improve."

    df["response_draft"] = df.apply(generate_reply, axis=1)

    st.subheader("✍️ Drafted Responses")
    st.dataframe(df[["member_id", "program", "feedback", "response_draft"]])
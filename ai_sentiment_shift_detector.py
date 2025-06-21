import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

def run():
    st.title("💬 AI Sentiment Shift Detector")

    uploaded = st.file_uploader("Upload member_feedback_history.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(10)],
            "previous_feedback": [
                "Loved the trainers and class options.",
                "Gym was okay but could use more equipment.",
                "I enjoyed the swim sessions a lot.",
                "Staff is friendly and helpful.",
                "Good facility but very crowded.",
                "Loved the community vibe.",
                "Wish the hours were longer.",
                "No complaints. It’s great.",
                "Too noisy sometimes.",
                "Excellent programs and staff."
            ],
            "recent_feedback": [
                "Not feeling as motivated lately.",
                "Still crowded and noisy at times.",
                "Trainers are still awesome.",
                "Thinking about pausing membership.",
                "Better class variety now.",
                "Community is still fun!",
                "Not using it as often now.",
                "Might switch gyms for variety.",
                "Still noisy and hot.",
                "Everything’s still great!"
            ]
        })

    st.subheader("📋 Feedback History")
    st.dataframe(df)

    df["prev_score"] = df["previous_feedback"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["recent_score"] = df["recent_feedback"].apply(lambda x: TextBlob(x).sentiment.polarity)
    df["sentiment_change"] = df["recent_score"] - df["prev_score"]

    st.subheader("📈 Sentiment Shift Analysis")
    st.dataframe(df[["member_id", "prev_score", "recent_score", "sentiment_change"]].sort_values("sentiment_change"))

    fig, ax = plt.subplots()
    df.set_index("member_id")[["prev_score", "recent_score"]].plot(kind="bar", ax=ax)
    ax.set_ylabel("Sentiment Score")
    ax.set_title("Sentiment Before vs. After")
    st.pyplot(fig)

    st.subheader("🚩 Members with Negative Sentiment Shift")
    st.dataframe(df[df["sentiment_change"] < -0.2][["member_id", "sentiment_change"]])
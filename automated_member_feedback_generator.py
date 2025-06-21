import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📬 Automated Member Feedback Generator")

    uploaded = st.file_uploader("Upload member_activity_summary.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(40)],
            "avg_visits": np.random.randint(1, 12, 40),
            "goal": np.random.choice(["Weight Loss", "Strength", "Wellness"], 40),
            "feedback_score": np.random.uniform(2.5, 5.0, 40).round(1)
        })

    def generate_feedback(row):
        if row["avg_visits"] >= 8:
            base = "You're showing great consistency!"
        elif row["avg_visits"] >= 4:
            base = "Nice job staying active! Keep pushing."
        else:
            base = "Let’s try to increase your visits — your goals are within reach."

        tone = "💪 You're on the right track!" if row["feedback_score"] > 4 else "🚀 Let's build momentum together!"
        return f"{base} Goal: {row['goal']}. {tone}"

    df["auto_feedback"] = df.apply(generate_feedback, axis=1)

    st.subheader("📝 Personalized Feedback Preview")
    st.dataframe(df[["member_id", "avg_visits", "goal", "feedback_score", "auto_feedback"]])
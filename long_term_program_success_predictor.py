import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📆 Long-Term Program Success Predictor")

    uploaded = st.file_uploader("Upload program_history.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "program_name": [f"Program {i}" for i in range(30)],
            "weeks": np.random.randint(4, 16, 30),
            "avg_attendance": np.random.randint(10, 40, 30),
            "completion_rate": np.random.uniform(0.6, 1.0, 30).round(2),
            "feedback_avg": np.random.uniform(3.0, 5.0, 30).round(1)
        })

    df["success_score"] = (df["completion_rate"] * 0.4 + df["feedback_avg"] / 5 * 0.3 + df["avg_attendance"] / 40 * 0.3).round(2)
    df["outlook"] = df["success_score"].apply(lambda x: "🚀 Excellent" if x > 0.8 else ("✅ Good" if x > 0.6 else "⚠️ Needs Review"))

    st.subheader("📊 Program Success Scores")
    st.dataframe(df.sort_values("success_score", ascending=False))
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🏅 Coach Performance Analyzer")

    uploaded = st.file_uploader("Upload coach_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "coach": [f"Coach {i}" for i in range(1, 21)],
            "feedback_score": np.round(np.random.uniform(3.0, 5.0, 20), 1),
            "win_rate": np.round(np.random.uniform(0.3, 0.9, 20), 2),
            "athlete_retention": np.round(np.random.uniform(0.5, 0.95, 20), 2)
        })

    st.subheader("📋 Coach Data")
    st.dataframe(df)

    df["performance_score"] = (
        df["feedback_score"] * 0.4 +
        df["win_rate"] * 0.3 +
        df["athlete_retention"] * 0.3
    ).round(2)

    st.subheader("🏆 Composite Scores")
    st.dataframe(df.sort_values("performance_score", ascending=False))

    fig, ax = plt.subplots()
    df.sort_values("performance_score", ascending=False).plot(
        x="coach", y="performance_score", kind="bar", ax=ax, legend=False, color="indigo"
    )
    ax.set_ylabel("Score")
    ax.set_title("Coach Performance Scores")
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📈 Instructor Performance Insight Dashboard")

    uploaded = st.file_uploader("Upload instructor_metrics.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "instructor": [f"Coach {i}" for i in range(10)],
            "avg_feedback": np.random.uniform(3.5, 5.0, 10).round(2),
            "avg_attendance": np.random.randint(10, 50, 10),
            "sessions_this_month": np.random.randint(8, 30, 10)
        })

    st.subheader("📋 Instructor Metrics")
    st.dataframe(df)

    df["performance_score"] = (
        df["avg_feedback"] * 0.5 +
        df["avg_attendance"] * 0.3 +
        df["sessions_this_month"] * 0.2
    ).round(1)

    st.subheader("🏆 Ranked Instructor Scores")
    st.dataframe(df.sort_values("performance_score", ascending=False))

    fig, ax = plt.subplots()
    df.set_index("instructor")["performance_score"].sort_values().plot(kind="barh", ax=ax, color="steelblue")
    ax.set_xlabel("Score")
    ax.set_title("Instructor Performance Ranking")
    st.pyplot(fig)
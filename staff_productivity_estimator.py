import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📋 Staff Productivity Estimator")

    uploaded = st.file_uploader("Upload staff_performance.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "name": [f"Staff_{i}" for i in range(1, 21)],
            "tasks_completed": np.random.randint(10, 100, 20),
            "hours_worked": np.random.randint(20, 50, 20),
            "feedback_score": np.round(np.random.uniform(3.0, 5.0, 20), 1)
        })

    st.subheader("📋 Staff Performance Data")
    st.dataframe(df)

    df["efficiency"] = df["tasks_completed"] / df["hours_worked"]
    df["productivity_score"] = (df["efficiency"] * 0.6 + df["feedback_score"] * 0.4).round(2)

    st.subheader("🏅 Productivity Scores")
    st.dataframe(df[["name", "tasks_completed", "hours_worked", "feedback_score", "productivity_score"]])

    top = df.sort_values("productivity_score", ascending=False).head(5)
    st.metric("Top Score", f"{top['productivity_score'].iloc[0]:.2f} ({top['name'].iloc[0]})")

    fig, ax = plt.subplots()
    df.sort_values("productivity_score", ascending=False).plot(
        x="name", y="productivity_score", kind="bar", ax=ax, legend=False, color="teal"
    )
    ax.set_title("Staff Productivity Ranking")
    st.pyplot(fig)
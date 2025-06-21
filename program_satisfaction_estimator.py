import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📋 Program Satisfaction Estimator")

    uploaded = st.file_uploader("Upload program_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "program": np.random.choice(["Yoga", "Basketball", "Swim Lessons", "Senior Fitness"], 200),
            "value_score": np.random.uniform(1.0, 5.0, 200).round(1),
            "enjoyment_score": np.random.uniform(1.0, 5.0, 200).round(1),
            "staff_score": np.random.uniform(1.0, 5.0, 200).round(1)
        })

    st.subheader("📋 Feedback Data")
    st.dataframe(df.head())

    df["satisfaction"] = df[["value_score", "enjoyment_score", "staff_score"]].mean(axis=1).round(2)
    avg_scores = df.groupby("program")["satisfaction"].mean().sort_values(ascending=False)

    st.subheader("🏆 Program Satisfaction Rankings")
    st.dataframe(avg_scores.reset_index())

    fig, ax = plt.subplots()
    avg_scores.plot(kind="bar", color="mediumseagreen", ax=ax)
    ax.set_ylabel("Avg. Satisfaction")
    ax.set_title("Average Satisfaction by Program")
    st.pyplot(fig)
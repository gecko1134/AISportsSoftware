import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎯 Goal Progress Evaluator AI")

    uploaded = st.file_uploader("Upload member_progress.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(40)],
            "goal_type": np.random.choice(["Weight Loss", "Strength", "Cardio"], 40),
            "goal_value": np.random.randint(5, 20, 40),
            "current_progress": np.random.randint(0, 20, 40)
        })

    df["progress_pct"] = (df["current_progress"] / df["goal_value"]).clip(0, 1).round(2)
    df["status"] = pd.cut(df["progress_pct"], bins=[-0.01, 0.5, 0.85, 1.0], labels=["Behind", "On Track", "Completed"])

    st.subheader("📊 Goal Achievement Summary")
    st.dataframe(df[["member_id", "goal_type", "goal_value", "current_progress", "progress_pct", "status"]])
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🗳️ Community Vote Outcome Predictor")

    uploaded = st.file_uploader("Upload vote_history.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "poll_id": [f"P{i//10}" for i in range(50)],
            "option": np.random.choice(["Yes", "No", "Maybe"], 50),
            "votes": np.random.randint(1, 20, 50)
        })

    summary = df.groupby(["poll_id", "option"])["votes"].sum().unstack().fillna(0)
    summary["predicted_outcome"] = summary.idxmax(axis=1)
    summary["margin"] = (summary.max(axis=1) - summary.min(axis=1)).round(1)

    st.subheader("📊 Predicted Outcomes by Poll")
    st.dataframe(summary)
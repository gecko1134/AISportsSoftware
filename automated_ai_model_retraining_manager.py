import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run():
    st.title("🧪 Automated AI Model Retraining Manager")

    uploaded = st.file_uploader("Upload model_metrics.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded, parse_dates=["last_trained"])
    else:
        now = datetime.today()
        df = pd.DataFrame({
            "model_name": [f"model_{i}" for i in range(8)],
            "accuracy": np.random.uniform(0.70, 0.98, 8).round(3),
            "drift_score": np.random.uniform(0.0, 1.0, 8).round(2),
            "last_trained": [now - timedelta(days=np.random.randint(10, 180)) for _ in range(8)]
        })

    st.subheader("📋 Model Performance Overview")
    st.dataframe(df)

    df["days_since_trained"] = (datetime.today() - df["last_trained"]).dt.days
    df["retrain_flag"] = (df["accuracy"] < 0.85) | (df["drift_score"] > 0.3) | (df["days_since_trained"] > 90)

    st.subheader("🔁 Retraining Recommendations")
    st.dataframe(df[df["retrain_flag"]][["model_name", "accuracy", "drift_score", "days_since_trained"]])

    st.metric("Models Needing Retrain", df["retrain_flag"].sum())
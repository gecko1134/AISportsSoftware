import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🛠️ Equipment Downtime Predictor")

    uploaded = st.file_uploader("Upload equipment_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "equipment_id": [f"E{i}" for i in range(100)],
            "hours_used": np.random.randint(100, 3000, 100),
            "failures_last_6mo": np.random.randint(0, 5, 100),
            "avg_repair_time": np.random.randint(1, 5, 100),
            "last_downtime_days": np.random.randint(1, 100, 100)
        })

    st.subheader("📋 Equipment Logs")
    st.dataframe(df.head())

    X = df[["hours_used", "failures_last_6mo", "avg_repair_time"]]
    y = df["last_downtime_days"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    df["predicted_downtime"] = model.predict(X)

    st.subheader("⚠️ High Downtime Risk")
    st.dataframe(df.sort_values("predicted_downtime", ascending=False).head(10)[["equipment_id", "predicted_downtime"]])

    fig, ax = plt.subplots()
    ax.hist(df["predicted_downtime"], bins=20, color="salmon")
    ax.set_xlabel("Predicted Downtime (days)")
    ax.set_title("Forecasted Equipment Downtime")
    st.pyplot(fig)
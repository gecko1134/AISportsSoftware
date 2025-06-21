import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

def run():
    st.title("🚗 Parking Demand Predictor")

    uploaded = st.file_uploader("Upload parking_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        from datetime import datetime, timedelta
        np.random.seed(42)
        base = datetime(2024, 1, 1)
        timestamps = [base + timedelta(minutes=np.random.randint(0, 60*24*60)) for _ in range(1000)]
        df = pd.DataFrame({"timestamp": timestamps})

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.dayofweek

    grouped = df.groupby(["hour", "weekday"]).size().reset_index(name="vehicles")

    X = grouped[["hour", "weekday"]]
    y = grouped["vehicles"]

    model = GradientBoostingRegressor()
    model.fit(X, y)
    grouped["predicted"] = model.predict(X)

    pivot = grouped.pivot(index="hour", columns="weekday", values="predicted")

    st.subheader("📈 Predicted Parking Demand (Hour x Weekday)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    ax.set_title("Forecasted Parking Volume")
    st.pyplot(fig)

    st.metric("Peak Predicted Volume", f"{int(grouped['predicted'].max())} vehicles/hour")
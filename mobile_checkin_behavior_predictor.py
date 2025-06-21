import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

def run():
    st.title("📱 Mobile Check-In Behavior Predictor")

    uploaded = st.file_uploader("Upload checkin_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        from datetime import datetime, timedelta
        np.random.seed(42)
        df = pd.DataFrame({
            "user_id": [f"U{i}" for i in range(1000)],
            "checkin_time": [datetime(2024, 6, 1) + timedelta(minutes=np.random.randint(6*60, 22*60)) for _ in range(1000)],
            "is_mobile": np.random.choice([1, 0], 1000, p=[0.6, 0.4]),
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 1000)
        })

    df["checkin_time"] = pd.to_datetime(df["checkin_time"])
    df["hour"] = df["checkin_time"].dt.hour
    df["tier_code"] = df["tier"].astype("category").cat.codes

    st.subheader("📋 Mobile Check-In Data")
    st.dataframe(df.head())

    mobile_df = df[df["is_mobile"] == 1]

    X = mobile_df[["tier_code"]]
    y = mobile_df["hour"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    mobile_df["predicted_hour"] = model.predict(X)

    avg_times = mobile_df.groupby("tier")["predicted_hour"].mean()

    st.subheader("⏰ Preferred Mobile Check-In Times (Predicted)")
    st.dataframe(avg_times.round(1).reset_index())

    fig, ax = plt.subplots()
    avg_times.plot(kind="bar", ax=ax, color="teal")
    ax.set_ylabel("Hour of Day")
    ax.set_title("Predicted Check-In Time by Tier")
    st.pyplot(fig)
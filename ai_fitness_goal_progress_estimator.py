import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🏋️ AI Fitness Goal Progress Estimator")

    uploaded = st.file_uploader("Upload fitness_tracking.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "user_id": [f"U{i}" for i in range(100)],
            "goal_type": np.random.choice(["Weight Loss", "Strength", "Endurance"], 100),
            "weeks_active": np.random.randint(1, 20, 100),
            "sessions": np.random.randint(3, 40, 100),
            "progress_pct": np.random.uniform(10, 100, 100).round(1)
        })

    st.subheader("📋 Fitness Goal Data")
    st.dataframe(df.head())

    df["goal_code"] = df["goal_type"].astype("category").cat.codes
    X = df[["weeks_active", "sessions", "goal_code"]]
    y = df["progress_pct"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    df["predicted_progress"] = model.predict(X).clip(0, 100).round(1)

    st.subheader("🎯 Predicted Progress Toward Goal")
    st.dataframe(df[["user_id", "goal_type", "predicted_progress"]].sort_values("predicted_progress", ascending=False))

    fig, ax = plt.subplots()
    ax.hist(df["predicted_progress"], bins=15, color="green")
    ax.set_xlabel("Progress (%)")
    ax.set_title("Distribution of Predicted Goal Completion")
    st.pyplot(fig)
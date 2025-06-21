import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🧒 AI Childcare Demand Forecaster")

    uploaded = st.file_uploader("Upload program_signups.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        programs = ["Fitness", "Yoga", "Swim", "Bootcamp"]
        df = pd.DataFrame({
            "program": np.random.choice(programs, 300),
            "hour": np.random.randint(6, 21, 300),
            "day_of_week": np.random.randint(0, 7, 300),
            "with_childcare": np.random.choice([0, 1], 300, p=[0.6, 0.4])
        })
        df["demand"] = df["with_childcare"] * np.random.randint(1, 4, 300)

    st.subheader("📋 Signup Data")
    st.dataframe(df.head())

    df["program_code"] = df["program"].astype("category").cat.codes
    X = df[["hour", "day_of_week", "program_code"]]
    y = df["demand"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    df["predicted"] = model.predict(X)

    st.subheader("📈 Forecasted Childcare Demand")
    pivot = df.pivot_table(index="hour", columns="day_of_week", values="predicted", aggfunc="mean").fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax)
    st.pyplot(fig)

    st.metric("Peak Forecasted Demand", f"{int(df['predicted'].max())} children/hour")
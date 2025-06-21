import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🎯 Youth Program Progress Forecaster")

    uploaded = st.file_uploader("Upload youth_development.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "age": np.random.randint(6, 16, 200),
            "sessions_attended": np.random.randint(5, 30, 200),
            "coach_score": np.random.uniform(3.0, 5.0, 200).round(1),
            "program_type": np.random.choice(["Team", "Clinic", "Recreation"], 200),
            "improvement_score": np.random.uniform(0.1, 1.0, 200).round(2)
        })

    st.subheader("📋 Youth Development Data")
    st.dataframe(df.head())

    df["program_code"] = df["program_type"].astype("category").cat.codes
    X = df[["age", "sessions_attended", "coach_score", "program_code"]]
    y = df["improvement_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    df["predicted"] = model.predict(X)

    st.subheader("📈 Actual vs Predicted Progress")
    fig, ax = plt.subplots()
    ax.scatter(df["improvement_score"], df["predicted"], alpha=0.6)
    ax.set_xlabel("Actual Score")
    ax.set_ylabel("Predicted Score")
    ax.set_title("Youth Progress Forecast")
    st.pyplot(fig)

    st.metric("Avg Predicted Progress", f"{df['predicted'].mean():.2f}")
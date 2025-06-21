import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🧑‍💻 Hybrid Class Attendance Forecaster")

    uploaded = st.file_uploader("Upload hybrid_sessions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "class_type": np.random.choice(["Yoga", "Bootcamp", "Cardio"], 200),
            "hour": np.random.randint(6, 20, 200),
            "weekday": np.random.randint(0, 7, 200),
            "instructor_rating": np.random.uniform(3.0, 5.0, 200),
            "in_person": np.random.randint(5, 30, 200),
            "virtual": np.random.randint(3, 20, 200)
        })

    st.subheader("📋 Hybrid Class Data")
    st.dataframe(df.head())

    df["type_code"] = df["class_type"].astype("category").cat.codes
    X = df[["hour", "weekday", "type_code", "instructor_rating"]]
    y_in = df["in_person"]
    y_virt = df["virtual"]

    X_train_in, X_test_in, y_train_in, y_test_in = train_test_split(X, y_in, test_size=0.3, random_state=42)
    X_train_virt, X_test_virt, y_train_virt, y_test_virt = train_test_split(X, y_virt, test_size=0.3, random_state=42)

    model_in = GradientBoostingRegressor().fit(X_train_in, y_train_in)
    model_virt = GradientBoostingRegressor().fit(X_train_virt, y_train_virt)

    df["predicted_in_person"] = model_in.predict(X)
    df["predicted_virtual"] = model_virt.predict(X)

    st.subheader("📈 Forecasted Attendance Split")
    forecast = df.groupby("class_type")[["predicted_in_person", "predicted_virtual"]].mean().round()
    st.dataframe(forecast)

    forecast.plot(kind="bar", stacked=True)
    st.pyplot(plt.gcf())
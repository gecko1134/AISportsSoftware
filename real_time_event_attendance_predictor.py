import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🎟️ Real-Time Event Attendance Predictor")

    uploaded = st.file_uploader("Upload event_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_type": np.random.choice(["Game", "Class", "Meetup", "Showcase"], 150),
            "registered": np.random.randint(20, 300, 150),
            "weekday": np.random.randint(0, 7, 150),
            "hour": np.random.randint(8, 21, 150),
            "forecast_temp": np.random.uniform(40, 90, 150),
            "forecast_rain": np.random.choice([0, 1], 150, p=[0.8, 0.2]),
            "actual_attendance": np.random.randint(10, 300, 150)
        })

    st.subheader("📋 Event Features & Attendance")
    st.dataframe(df.head())

    df["event_code"] = df["event_type"].astype("category").cat.codes
    X = df[["event_code", "registered", "weekday", "hour", "forecast_temp", "forecast_rain"]]
    y = df["actual_attendance"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    df["predicted_attendance"] = model.predict(X).round()

    st.subheader("📈 Forecasted Event Turnout")
    st.dataframe(df[["event_type", "registered", "predicted_attendance"]].sort_values("predicted_attendance", ascending=False))

    fig, ax = plt.subplots()
    df.plot.scatter(x="registered", y="predicted_attendance", ax=ax, color="teal")
    ax.set_title("Registration vs. Forecasted Attendance")
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def run():
    st.title("📅 Seasonal Demand Forecaster")

    uploaded = st.file_uploader("Upload monthly_activity.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        months = pd.date_range("2023-01-01", periods=24, freq="M")
        df = pd.DataFrame({
            "month": np.tile(months, 3),
            "program": np.repeat(["Yoga", "Swim", "Basketball"], 24),
            "attendees": np.random.randint(50, 300, 72)
        })

    df["month"] = pd.to_datetime(df["month"])
    df["month_num"] = df["month"].dt.month + 12 * (df["month"].dt.year - df["month"].dt.year.min())
    df["season"] = df["month"].dt.month % 12 // 3 + 1  # 1=Winter, ..., 4=Fall
    df["season_name"] = df["season"].map({1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"})

    st.subheader("📋 Program Activity by Month")
    st.dataframe(df.head())

    program = st.selectbox("Select Program", sorted(df["program"].unique()))
    prog_df = df[df["program"] == program]

    X = prog_df[["month_num"]]
    y = prog_df["attendees"]
    model = LinearRegression().fit(X, y)
    prog_df["forecast"] = model.predict(X)

    st.subheader("📈 Demand Forecast")
    fig, ax = plt.subplots()
    ax.plot(prog_df["month"], prog_df["attendees"], label="Actual", marker="o")
    ax.plot(prog_df["month"], prog_df["forecast"], label="Forecast", linestyle="--")
    ax.set_title(f"{program} Attendance Forecast")
    ax.legend()
    st.pyplot(fig)

    season_avg = prog_df.groupby("season_name")["attendees"].mean().round()
    st.subheader("📊 Seasonal Average Attendance")
    st.bar_chart(season_avg)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def run():
    st.title("📊 User Engagement Forecaster")

    uploaded = st.file_uploader("Upload engagement_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        from datetime import datetime, timedelta
        base = datetime(2023, 1, 1)
        dates = [base + timedelta(days=i) for i in range(180)]
        usage = np.random.poisson(lam=50, size=len(dates)) + np.linspace(0, 30, len(dates)).astype(int)
        df = pd.DataFrame({"date": dates, "sessions": usage})

    st.subheader("📅 Engagement Data")
    st.dataframe(df.head())

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["days"] = (df["date"] - df["date"].min()).dt.days

    model = LinearRegression()
    model.fit(df[["days"]], df["sessions"])
    df["predicted"] = model.predict(df[["days"]])

    st.subheader("📈 Engagement Forecast")
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["sessions"], label="Actual")
    ax.plot(df["date"], df["predicted"], linestyle="--", label="Forecast", color="orange")
    ax.set_ylabel("Sessions")
    ax.set_title("Engagement Trend")
    ax.legend()
    st.pyplot(fig)

    st.metric("Trend Rate", f"{model.coef_[0]:.2f} sessions/day")
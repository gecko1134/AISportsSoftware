import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def run():
    st.title("💪 AI Fitness Progress Tracker")

    uploaded = st.file_uploader("Upload fitness_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        import random
        from datetime import datetime, timedelta

        users = [f"user_{i}" for i in range(1, 21)]
        records = []
        base_date = datetime(2024, 1, 1)
        for u in users:
            for i in range(10):
                date = base_date + timedelta(days=i * 7)
                weight = random.uniform(60, 90) - i * 0.3 + random.uniform(-0.5, 0.5)
                records.append({"user_id": u, "date": date, "weight": round(weight, 1)})

        df = pd.DataFrame(records)

    st.subheader("📋 Fitness Log")
    st.dataframe(df.head())

    df["date"] = pd.to_datetime(df["date"])
    selected_user = st.selectbox("Select User", sorted(df["user_id"].unique()))

    user_df = df[df["user_id"] == selected_user].sort_values("date")
    st.line_chart(user_df.set_index("date")["weight"])

    X = (user_df["date"] - user_df["date"].min()).dt.days.values.reshape(-1, 1)
    y = user_df["weight"].values
    model = LinearRegression().fit(X, y)
    slope = model.coef_[0]

    st.metric("Weight Trend (kg/week)", f"{slope * 7:.2f}")
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🎟️ Event Ticket Price Optimizer")

    uploaded = st.file_uploader("Upload ticket_sales.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "event_type": np.random.choice(["Concert", "Game", "Workshop"], 200),
            "base_price": np.random.randint(10, 50, 200),
            "time_to_event_days": np.random.randint(1, 30, 200),
            "attendees": np.random.randint(50, 500, 200),
            "revenue": np.random.randint(1000, 20000, 200)
        })

    st.subheader("📋 Ticket Sales Data")
    st.dataframe(df.head())

    df["event_code"] = df["event_type"].astype("category").cat.codes
    X = df[["base_price", "time_to_event_days", "attendees", "event_code"]]
    y = df["revenue"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    df["predicted_revenue"] = model.predict(X)

    price_range = np.arange(10, 101, 5)
    test_input = pd.DataFrame({
        "base_price": price_range,
        "time_to_event_days": [7]*len(price_range),
        "attendees": [250]*len(price_range),
        "event_code": [1]*len(price_range)
    })
    forecast = model.predict(test_input)

    st.subheader("📈 Suggested Price vs Revenue")
    fig, ax = plt.subplots()
    ax.plot(price_range, forecast, marker="o")
    ax.set_xlabel("Ticket Price ($)")
    ax.set_ylabel("Predicted Revenue ($)")
    ax.set_title("Optimal Ticket Price Range")
    st.pyplot(fig)
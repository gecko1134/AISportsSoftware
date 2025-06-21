import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

def run():
    st.title("🍿 Concession Sales Forecaster")

    uploaded = st.file_uploader("Upload sales_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        items = ["Water", "Soda", "Popcorn", "Nachos", "Hotdog", "Protein Bar"]
        df = pd.DataFrame({
            "item": np.random.choice(items, 200),
            "hour": np.random.randint(10, 22, 200),
            "weekday": np.random.randint(0, 7, 200),
            "sold": np.random.randint(5, 150, 200)
        })

    st.subheader("📋 Concession Sales Logs")
    st.dataframe(df.head())

    df["item_code"] = df["item"].astype("category").cat.codes
    X = df[["item_code", "hour", "weekday"]]
    y = df["sold"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    df["forecasted_sales"] = model.predict(X).round()

    top_items = df.groupby("item")["forecasted_sales"].mean().sort_values(ascending=False).reset_index()

    st.subheader("📈 Forecasted High-Demand Items")
    st.dataframe(top_items)

    fig, ax = plt.subplots()
    top_items.plot(kind="bar", x="item", y="forecasted_sales", ax=ax, color="tomato", legend=False)
    ax.set_ylabel("Avg Forecasted Sales")
    ax.set_title("Predicted Concession Demand")
    st.pyplot(fig)
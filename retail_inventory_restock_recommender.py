import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🛍️ Retail Inventory Restock Recommender")

    uploaded = st.file_uploader("Upload retail_sales.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "item": np.random.choice(["Shirt", "Towel", "Bottle", "Shoes", "Cap"], 200),
            "week": np.random.randint(1, 53, 200),
            "units_sold": np.random.randint(5, 100, 200),
            "stock_left": np.random.randint(0, 30, 200),
            "season": np.random.choice(["Spring", "Summer", "Fall", "Winter"], 200)
        })

    st.subheader("📋 Retail Sales Logs")
    st.dataframe(df.head())

    df["item_code"] = df["item"].astype("category").cat.codes
    df["season_code"] = df["season"].astype("category").cat.codes
    X = df[["item_code", "week", "season_code", "stock_left"]]
    y = df["units_sold"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    df["forecast_units"] = model.predict(X).round()

    df_summary = df.groupby("item")[["units_sold", "forecast_units", "stock_left"]].mean().round().sort_values("forecast_units", ascending=False)
    df_summary["restock_urgency"] = (df_summary["forecast_units"] > df_summary["stock_left"]).map({True: "⚠️ Urgent", False: "OK"})

    st.subheader("📦 Restock Forecast Summary")
    st.dataframe(df_summary)

    fig, ax = plt.subplots()
    df_summary["forecast_units"].plot(kind="bar", ax=ax, color="darkorange")
    ax.set_ylabel("Avg Forecast Sales")
    ax.set_title("Predicted Demand by Item")
    st.pyplot(fig)
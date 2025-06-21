import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("💰 Equipment Replacement Budget Estimator")

    uploaded = st.file_uploader("Upload equipment_inventory.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "equipment_id": [f"E{i}" for i in range(100)],
            "age_years": np.random.randint(1, 10, 100),
            "hours_used": np.random.randint(100, 5000, 100),
            "repairs_last_year": np.random.randint(0, 5, 100),
            "replacement_cost": np.random.randint(1000, 10000, 100)
        })

    st.subheader("📋 Equipment Inventory")
    st.dataframe(df.head())

    X = df[["age_years", "hours_used", "repairs_last_year"]]
    y = df["replacement_cost"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    df["predicted_cost"] = model.predict(X).clip(1000, 10000).round()

    st.subheader("📈 Forecasted Replacement Cost")
    st.dataframe(df[["equipment_id", "age_years", "hours_used", "repairs_last_year", "predicted_cost"]].sort_values("predicted_cost", ascending=False))

    fig, ax = plt.subplots()
    df["predicted_cost"].hist(bins=15, ax=ax, color="orange")
    ax.set_title("Replacement Budget Forecast")
    ax.set_xlabel("Predicted Cost ($)")
    st.pyplot(fig)

    st.metric("Total Budget Forecast", f"${df['predicted_cost'].sum():,.0f}")
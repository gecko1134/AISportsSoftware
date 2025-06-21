import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🛠️ Maintenance Cost Forecaster")

    uploaded = st.file_uploader("Upload maintenance_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "facility_id": np.random.randint(1, 6, 200),
            "age_years": np.random.randint(1, 20, 200),
            "usage_hours": np.random.randint(50, 1000, 200),
            "prev_cost": np.random.randint(100, 5000, 200),
            "repair_cost": np.random.randint(200, 10000, 200)
        })

    st.subheader("📋 Maintenance Data")
    st.dataframe(df.head())

    X = df[["age_years", "usage_hours", "prev_cost"]]
    y = df["repair_cost"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    df["predicted"] = model.predict(X)

    st.subheader("📈 Actual vs Predicted Repair Cost")
    fig, ax = plt.subplots()
    ax.scatter(df["repair_cost"], df["predicted"], alpha=0.6)
    ax.set_xlabel("Actual Cost")
    ax.set_ylabel("Predicted Cost")
    ax.set_title("Maintenance Cost Forecast")
    st.pyplot(fig)

    st.metric("Average Forecasted Cost", f"${df['predicted'].mean():,.0f}")
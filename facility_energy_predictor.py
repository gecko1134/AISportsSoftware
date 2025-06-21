import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("⚡ Facility Energy Usage Predictor")

    st.write("Estimate energy cost based on usage hours, lighting type, and facility size.")

    # Generate synthetic data
    np.random.seed(42)
    df = pd.DataFrame({
        "hours": np.random.randint(2, 12, 100),
        "size_sqft": np.random.randint(3000, 12000, 100),
        "lighting_type": np.random.choice(["LED", "Halogen", "Fluorescent"], 100),
        "energy_cost": np.nan
    })

    df["type_code"] = df["lighting_type"].map({"LED": 1, "Halogen": 2, "Fluorescent": 1.5})
    df["energy_cost"] = 0.08 * df["hours"] * df["size_sqft"] * df["type_code"]

    st.subheader("🧪 Sample Data")
    st.dataframe(df.head())

    X = df[["hours", "size_sqft", "type_code"]]
    y = df["energy_cost"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    st.subheader("📉 Actual vs Predicted Cost")
    fig, ax = plt.subplots()
    ax.scatter(y_test, pred, alpha=0.7)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], "--", color="gray")
    ax.set_xlabel("Actual Cost")
    ax.set_ylabel("Predicted Cost")
    st.pyplot(fig)

    st.metric("Avg. Energy Cost Prediction", f"${pred.mean():.2f}")
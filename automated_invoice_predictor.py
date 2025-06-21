import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("📥 Automated Invoice Predictor")

    uploaded = st.file_uploader("Upload member_charges.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "sessions": np.random.randint(1, 15, 100),
            "addons": np.random.randint(0, 5, 100),
            "last_invoice": np.random.uniform(50, 300, 100).round(2)
        })

    st.subheader("📋 Member Charge History")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    X = df[["tier_code", "sessions", "addons"]]
    y = df["last_invoice"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    df["predicted_invoice"] = model.predict(X)

    st.subheader("💳 Forecasted Invoices")
    st.dataframe(df[["member_id", "tier", "sessions", "addons", "predicted_invoice"]].round(2))

    fig, ax = plt.subplots()
    df["predicted_invoice"].hist(bins=20, ax=ax, color="skyblue")
    ax.set_title("Predicted Invoice Distribution")
    ax.set_xlabel("Amount ($)")
    st.pyplot(fig)
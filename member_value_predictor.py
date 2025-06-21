import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("💎 Member Value Predictor (LTV)")

    uploaded = st.file_uploader("Upload members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("members.csv")

    st.subheader("📋 Member Data")
    st.dataframe(df.head())

    df["days_since_join"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["join_date"])).dt.days
    df["days_since_last"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["last_visit"])).dt.days
    df["tier_code"] = df["tier"].astype("category").cat.codes

    # Synthetic target: LTV = function of age, tier, tenure
    df["ltv"] = 50 * df["tier_code"] + (df["days_since_join"] - df["days_since_last"]) * 0.3 + np.random.normal(100, 50, len(df))

    X = df[["age", "days_since_join", "days_since_last", "tier_code"]]
    y = df["ltv"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    df["predicted_ltv"] = model.predict(X)

    st.subheader("💰 Top Members by Predicted LTV")
    st.dataframe(df[["name", "tier", "predicted_ltv"]].sort_values("predicted_ltv", ascending=False).head(10))

    st.subheader("📉 LTV Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["predicted_ltv"], bins=20, color="gold")
    ax.set_title("Predicted Lifetime Value Distribution")
    st.pyplot(fig)
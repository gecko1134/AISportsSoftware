import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("👨‍👩‍👧 Family Account Activity Forecaster")

    uploaded = st.file_uploader("Upload family_accounts.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "family_id": [f"FAM{i}" for i in range(100)],
            "num_members": np.random.randint(2, 6, 100),
            "avg_age": np.random.uniform(8, 45, 100),
            "past_30_day_sessions": np.random.randint(5, 40, 100)
        })

    st.subheader("📋 Family Account Data")
    st.dataframe(df.head())

    X = df[["num_members", "avg_age"]]
    y = df["past_30_day_sessions"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    df["predicted_sessions"] = model.predict(X).round()

    st.subheader("📈 Predicted Family Usage")
    st.dataframe(df[["family_id", "num_members", "avg_age", "predicted_sessions"]].sort_values("predicted_sessions", ascending=False).head(10))

    fig, ax = plt.subplots()
    df["predicted_sessions"].hist(bins=20, color="skyblue", ax=ax)
    ax.set_title("Forecasted 30-Day Family Usage")
    ax.set_xlabel("Sessions")
    st.pyplot(fig)
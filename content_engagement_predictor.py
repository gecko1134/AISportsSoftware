import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("📬 Content Engagement Predictor")

    uploaded = st.file_uploader("Upload content_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "type": np.random.choice(["Email", "Social Post", "Text Alert"], 200),
            "audience_size": np.random.randint(50, 5000, 200),
            "day_of_week": np.random.randint(0, 7, 200),
            "hour": np.random.randint(6, 22, 200),
            "engagement_score": np.random.uniform(0.1, 1.0, 200)
        })

    st.subheader("📋 Content Log")
    st.dataframe(df.head())

    df["type_code"] = df["type"].astype("category").cat.codes

    X = df[["audience_size", "day_of_week", "hour", "type_code"]]
    y = df["engagement_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    df["predicted"] = model.predict(X)

    st.subheader("📈 Predicted vs Actual Engagement")
    fig, ax = plt.subplots()
    ax.scatter(df["engagement_score"], df["predicted"], alpha=0.6)
    ax.set_xlabel("Actual Engagement")
    ax.set_ylabel("Predicted Engagement")
    ax.set_title("Engagement Prediction")
    st.pyplot(fig)

    st.metric("Top Predicted Engagement", f"{df['predicted'].max():.2f}")
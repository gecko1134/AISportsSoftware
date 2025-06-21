import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def run():
    st.title("🤝 Member Referral Influencer Model")

    uploaded = st.file_uploader("Upload member_referrals.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "referrals": np.random.randint(1, 10, 100),
            "referral_conversion_rate": np.random.uniform(0.1, 1.0, 100),
            "total_activity_score": np.random.randint(10, 100, 100),
            "future_growth_influence": np.random.uniform(1.0, 10.0, 100)
        })

    st.subheader("📋 Referral Data")
    st.dataframe(df.head())

    X = df[["referrals", "referral_conversion_rate", "total_activity_score"]]
    y = df["future_growth_influence"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    df["influence_score"] = model.predict(X)

    st.subheader("🏆 Top Referral Influencers")
    st.dataframe(df.sort_values("influence_score", ascending=False).head(10)[["member_id", "influence_score"]])

    fig, ax = plt.subplots()
    ax.bar(df["member_id"].head(15), df["influence_score"].head(15), color="orange")
    ax.set_ylabel("Influence Score")
    ax.set_title("Top Referral Drivers")
    st.pyplot(fig)
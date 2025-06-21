import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("🏅 Loyalty Rewards Gamification Predictor")

    uploaded = st.file_uploader("Upload loyalty_rewards_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        types = ["Badge", "Free Class", "VIP Day", "Points Bonus", "Leaderboard"]
        df = pd.DataFrame({
            "reward_type": np.random.choice(types, 200),
            "redeemed": np.random.randint(10, 1000, 200),
            "sessions_following_reward": np.random.randint(1, 20, 200)
        })

    st.subheader("📋 Reward Engagement Logs")
    st.dataframe(df.head())

    df["type_code"] = df["reward_type"].astype("category").cat.codes
    X = df[["type_code", "redeemed"]]
    y = df["sessions_following_reward"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    df["predicted_sessions"] = model.predict(X).round()

    top_rewards = df.groupby("reward_type")[["predicted_sessions"]].mean().sort_values("predicted_sessions", ascending=False).reset_index()
    st.subheader("🎯 Gamification Impact by Reward Type")
    st.dataframe(top_rewards)

    fig, ax = plt.subplots()
    top_rewards.set_index("reward_type").plot(kind="bar", ax=ax, legend=False, color="darkorange")
    ax.set_ylabel("Forecasted Sessions After Reward")
    ax.set_title("Engagement Score by Reward Type")
    st.pyplot(fig)
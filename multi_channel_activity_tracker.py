import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("📶 Multi-Channel Activity Tracker")

    uploaded = st.file_uploader("Upload user_activity.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "user_id": [f"U{i}" for i in range(1, 201)],
            "app_logins": np.random.poisson(5, 200),
            "kiosk_uses": np.random.poisson(3, 200),
            "in_person_visits": np.random.poisson(7, 200)
        })

    st.subheader("📋 Multi-Source User Activity")
    st.dataframe(df.head())

    df["total_touchpoints"] = df[["app_logins", "kiosk_uses", "in_person_visits"]].sum(axis=1)
    df["channel_mix_score"] = df[["app_logins", "kiosk_uses", "in_person_visits"]].std(axis=1)

    st.subheader("📊 Engagement Channel Mix")
    fig, ax = plt.subplots()
    sns.heatmap(df[["app_logins", "kiosk_uses", "in_person_visits"]].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.subheader("🧭 Top Diversified Users")
    top_diverse = df.sort_values("channel_mix_score", ascending=False).head(10)
    st.dataframe(top_diverse[["user_id", "app_logins", "kiosk_uses", "in_person_visits", "channel_mix_score"]])
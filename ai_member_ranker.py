import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("🎯 Member Engagement Ranker")

    uploaded = st.file_uploader("Upload members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("members.csv")

    st.subheader("📋 Member Data")
    st.dataframe(df.head())

    # Features: recency, age, tier
    df["days_since_last"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["last_visit"])).dt.days
    df["days_since_join"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["join_date"])).dt.days
    df["tier_code"] = df["tier"].astype("category").cat.codes

    features = df[["days_since_last", "days_since_join", "age", "tier_code"]]
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(features)

    # Engagement score = inverse of days_since_last + tier weight
    df["engagement_score"] = 1 - df_scaled[:, 0] + df_scaled[:, 3]
    df["engagement_score"] = df["engagement_score"].round(2)

    st.subheader("🏅 Ranked Members")
    ranked = df.sort_values("engagement_score", ascending=False).head(10)
    st.dataframe(ranked[["name", "tier", "engagement_score"]])

    st.subheader("📈 Score Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["engagement_score"], kde=True, ax=ax, color="skyblue")
    st.pyplot(fig)
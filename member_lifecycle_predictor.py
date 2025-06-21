import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🔄 Member Lifecycle Predictor")

    uploaded = st.file_uploader("Upload members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("members.csv")

    st.subheader("📋 Member Data")
    st.dataframe(df.head())

    df["days_since_join"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["join_date"])).dt.days
    df["tenure_group"] = pd.cut(df["days_since_join"], bins=[0, 180, 365, 1000], labels=["New", "Mid", "Loyal"])
    df["tier"] = df["tier"].astype("category")

    st.subheader("📊 Tenure by Tier")
    pivot = pd.crosstab(df["tenure_group"], df["tier"])
    st.dataframe(pivot)

    fig, ax = plt.subplots()
    pivot.plot(kind="bar", stacked=True, colormap="viridis", ax=ax)
    ax.set_title("Member Tenure Distribution by Tier")
    ax.set_ylabel("Members")
    st.pyplot(fig)

    st.markdown("Use this insight to tailor upgrades, retention campaigns, and rewards per lifecycle stage.")
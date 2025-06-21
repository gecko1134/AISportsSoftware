import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🎁 Loyalty Program Optimizer")

    uploaded = st.file_uploader("Upload members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": range(1000, 1100),
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "visits_last_90": np.random.randint(5, 40, 100),
            "total_spend": np.random.randint(100, 2000, 100),
            "downgraded": np.random.choice([0, 1], 100, p=[0.85, 0.15])
        })

    st.subheader("📋 Member Data")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    df["score"] = df["visits_last_90"] * 0.4 + df["total_spend"] * 0.6

    rules = pd.DataFrame({
        "Tier": ["Silver", "Gold", "VIP"],
        "Min Score": [0, 500, 1000],
        "Rewards": ["5% off", "1 free guest/month", "Monthly gift + VIP access"]
    })

    st.subheader("🛠 Suggested Tier Thresholds")
    st.dataframe(rules)

    fig, ax = plt.subplots()
    df.boxplot(column="score", by="tier", ax=ax, grid=False)
    ax.set_title("Score Distribution by Tier")
    ax.set_ylabel("Loyalty Score")
    st.pyplot(fig)
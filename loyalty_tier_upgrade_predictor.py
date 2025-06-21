import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎖️ Loyalty Tier Upgrade Predictor")

    uploaded = st.file_uploader("Upload member_tiers.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(50)],
            "current_tier": np.random.choice(["Silver", "Gold"], 50),
            "months_active": np.random.randint(1, 36, 50),
            "avg_spend": np.random.randint(30, 150, 50),
            "referrals": np.random.randint(0, 10, 50)
        })

    df["upgrade_score"] = (df["months_active"] * 0.3 + df["avg_spend"] * 0.4 + df["referrals"] * 2).round(1)
    df["upgrade_likelihood"] = pd.cut(df["upgrade_score"], bins=[0, 40, 70, 100, 200], labels=["Low", "Moderate", "High", "Very High"])

    st.subheader("📈 Upgrade Likelihood Scores")
    st.dataframe(df[["member_id", "current_tier", "upgrade_score", "upgrade_likelihood"]])
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎖️ Long-Term Loyalty Scorer")

    uploaded = st.file_uploader("Upload loyalty_members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "months_active": np.random.randint(6, 72, 100),
            "avg_monthly_visits": np.random.randint(1, 20, 100),
            "avg_feedback_score": np.random.uniform(3.0, 5.0, 100),
            "referrals": np.random.randint(0, 5, 100)
        })

    st.subheader("📋 Loyalty Inputs")
    st.dataframe(df.head())

    df["loyalty_score"] = (
        df["months_active"] * 0.3 +
        df["avg_monthly_visits"] * 0.2 +
        df["avg_feedback_score"] * 10 * 0.3 +
        df["referrals"] * 5 * 0.2
    ).round(1)

    def assign_tier(score):
        if score > 90:
            return "Platinum"
        elif score > 70:
            return "Gold"
        elif score > 50:
            return "Silver"
        else:
            return "Bronze"

    df["suggested_tier"] = df["loyalty_score"].apply(assign_tier)

    st.subheader("🏅 Loyalty Tier Recommendations")
    st.dataframe(df[["member_id", "loyalty_score", "suggested_tier"]].sort_values("loyalty_score", ascending=False))
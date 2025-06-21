import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📣 Reengagement Campaign Selector")

    uploaded = st.file_uploader("Upload inactive_members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"LM{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "last_visit_days": np.random.randint(30, 180, 100),
            "reason_lapsed": np.random.choice(["Cost", "Schedule", "Moved", "Motivation"], 100),
            "total_spend": np.random.randint(100, 2000, 100)
        })

    st.subheader("📋 Inactive Member Data")
    st.dataframe(df.head())

    def assign_campaign(row):
        if row["reason_lapsed"] == "Cost":
            return "10% Off Comeback Pass"
        elif row["reason_lapsed"] == "Schedule":
            return "Flexible Pass + Anytime App"
        elif row["reason_lapsed"] == "Moved":
            return "Virtual Program Invite"
        else:
            return "Motivation Boost Series"

    df["recommended_campaign"] = df.apply(assign_campaign, axis=1)

    st.subheader("💌 Suggested Reactivation Campaigns")
    st.dataframe(df[["member_id", "reason_lapsed", "recommended_campaign"]])
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("👑 VIP Experience Optimizer")

    uploaded = st.file_uploader("Upload vip_feedback.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "vip_id": [f"V{i}" for i in range(100)],
            "avg_weekly_visits": np.random.randint(2, 10, 100),
            "satisfaction_score": np.random.uniform(3.0, 5.0, 100).round(1),
            "used_upsells": np.random.randint(0, 4, 100),
            "feedback_note": np.random.choice(["wants more perks", "happy", "needs flexibility", "suggests app improvements"], 100)
        })

    st.subheader("📋 VIP Activity & Feedback")
    st.dataframe(df.head())

    df["vip_score"] = (
        df["avg_weekly_visits"] * 0.4 +
        df["satisfaction_score"] * 2 * 0.4 +
        df["used_upsells"] * 2 * 0.2
    ).round(1)

    def suggest_perk(row):
        if row["feedback_note"] == "wants more perks":
            return "Free Massage Add-on"
        elif row["feedback_note"] == "needs flexibility":
            return "Anytime Booking Upgrade"
        elif row["feedback_note"] == "suggests app improvements":
            return "App Beta Access + Perk"
        else:
            return "Surprise Wellness Gift"

    df["recommended_perk"] = df.apply(suggest_perk, axis=1)

    st.subheader("🌟 VIP Optimization Suggestions")
    st.dataframe(df[["vip_id", "vip_score", "recommended_perk"]].sort_values("vip_score", ascending=False))
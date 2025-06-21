import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🤝 Partner Program Integrator")

    uploaded = st.file_uploader("Upload partner_programs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "partner_name": ["City School", "Youth Soccer Assoc", "YMCA League"],
            "participants": np.random.randint(50, 500, 3),
            "referrals": np.random.randint(10, 100, 3),
            "program_type": ["Education", "Athletics", "Community"]
        })

    df["impact_score"] = (df["participants"] * 0.8 + df["referrals"] * 1.2).round(1)

    st.subheader("📋 Partner Engagement Overview")
    st.dataframe(df.sort_values(by="impact_score", ascending=False))
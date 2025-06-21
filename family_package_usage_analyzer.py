import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("👨‍👩‍👧‍👦 Family Package Usage Analyzer")

    uploaded = st.file_uploader("Upload family_memberships.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "family_id": [f"F{i}" for i in range(30)],
            "num_members": np.random.randint(2, 6, 30),
            "total_visits": np.random.randint(10, 200, 30),
            "kids_usage_pct": np.random.uniform(0.2, 0.8, 30).round(2),
            "adult_usage_pct": np.random.uniform(0.2, 0.8, 30).round(2)
        })

    df["visits_per_person"] = (df["total_visits"] / df["num_members"]).round(1)
    df["flag"] = df["visits_per_person"].apply(lambda x: "⚠️ Underutilized" if x < 5 else ("🔥 High Use" if x > 15 else "✅ Normal"))

    st.subheader("📋 Family Membership Usage Overview")
    st.dataframe(df)
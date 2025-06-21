import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("♿ Accessibility Checker AI")

    uploaded = st.file_uploader("Upload facility_zones.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "zone": ["Entrance", "Lobby", "Court A", "Turf Field", "Track", "Cafe", "Locker Room"],
            "ramp_access": np.random.choice([1, 0], 7),
            "restroom_nearby": np.random.choice([1, 0], 7),
            "signage_clear": np.random.choice([1, 0], 7)
        })

    st.subheader("📋 Zone Accessibility Inputs")
    st.dataframe(df)

    df["score"] = df[["ramp_access", "restroom_nearby", "signage_clear"]].sum(axis=1)
    df["status"] = df["score"].apply(lambda x: "✅ Good" if x == 3 else ("⚠️ Needs Attention" if x == 2 else "❌ Poor"))

    st.subheader("🔎 Accessibility Evaluation")
    st.dataframe(df[["zone", "score", "status"]].sort_values(by="score"))
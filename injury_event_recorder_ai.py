import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🩹 Injury Event Recorder AI")

    uploaded = st.file_uploader("Upload injury_reports.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=20),
            "location": np.random.choice(["Court", "Turf", "Track", "Locker Room"], 20),
            "injury_type": np.random.choice(["Sprain", "Fall", "Collision", "Strain"], 20),
            "severity": np.random.choice(["Low", "Moderate", "High"], 20),
            "reported_by": np.random.choice(["Coach", "Staff", "Member"], 20)
        })

    df["ai_tag"] = df.apply(lambda x: "⚠️ Flag for Review" if x["severity"] == "High" or x["location"] == "Locker Room" else "✅ Logged", axis=1)

    st.subheader("📋 Injury Log with AI Tags")
    st.dataframe(df)
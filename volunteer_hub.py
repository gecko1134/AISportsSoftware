import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🙋 Volunteer Hub")

    uploaded = st.file_uploader("Upload volunteer_signups.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "volunteer_id": [f"V{i}" for i in range(30)],
            "name": [f"Volunteer {i}" for i in range(30)],
            "preferred_shift": np.random.choice(["Morning", "Afternoon", "Evening"], 30),
            "assigned_role": np.random.choice(["Check-In", "Concessions", "Coach Helper", "Clean-Up"], 30),
        })

    st.subheader("📋 Volunteer Schedule & Roles")
    st.dataframe(df)

    shift_summary = df.groupby("preferred_shift")["assigned_role"].value_counts().unstack().fillna(0)
    st.subheader("📊 Shift-Roles Matrix")
    st.dataframe(shift_summary)

    if st.checkbox("Show All Assigned Volunteers"):
        for _, row in df.iterrows():
            st.markdown(f"✅ **{row['name']}** - {row['preferred_shift']} / {row['assigned_role']}")
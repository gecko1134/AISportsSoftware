import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("👤 User Admin Panel")

    uploaded = st.file_uploader("Upload users.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "user_id": [f"U{i}" for i in range(50)],
            "name": [f"User {i}" for i in range(50)],
            "role": np.random.choice(["Member", "Staff", "Admin"], 50),
            "status": np.random.choice(["Active", "Suspended"], 50)
        })

    st.subheader("📋 User Directory")
    st.dataframe(df)

    if st.checkbox("Show Admins Only"):
        df = df[df["role"] == "Admin"]

    st.subheader("🔄 Role or Status Editor (Simulated)")
    selected_user = st.selectbox("Select User ID", df["user_id"])
    new_role = st.selectbox("Change Role To", ["Member", "Staff", "Admin"])
    new_status = st.selectbox("Change Status To", ["Active", "Suspended"])

    if st.button("Apply Changes"):
        st.success(f"✅ Updated {selected_user} role to '{new_role}' and status to '{new_status}' (simulated)")
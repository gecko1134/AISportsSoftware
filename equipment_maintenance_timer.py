import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run():
    st.title("🔧 Equipment Maintenance Timer")

    uploaded = st.file_uploader("Upload equipment_inventory.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        now = datetime(2024, 6, 1)
        df = pd.DataFrame({
            "equipment_id": [f"EQ_{i}" for i in range(1, 31)],
            "type": np.random.choice(["Cardio", "Strength", "Mobility"], 30),
            "hours_used": np.random.randint(100, 3000, 30),
            "last_maintenance": [now - timedelta(days=np.random.randint(15, 120)) for _ in range(30)]
        })

    st.subheader("📋 Equipment Inventory")
    st.dataframe(df)

    df["days_since_last"] = (datetime(2024, 6, 1) - pd.to_datetime(df["last_maintenance"])).dt.days
    df["maintenance_interval_days"] = (df["hours_used"] / 10).clip(30, 90).round()
    df["next_due_in"] = df["maintenance_interval_days"] - df["days_since_last"]
    df["next_due_in"] = df["next_due_in"].apply(lambda x: max(x, 0))

    st.subheader("🗓️ Maintenance Schedule")
    st.dataframe(df[["equipment_id", "type", "hours_used", "days_since_last", "maintenance_interval_days", "next_due_in"]].sort_values("next_due_in"))
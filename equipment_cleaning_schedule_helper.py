import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🧼 Equipment Cleaning Schedule Helper")

    uploaded = st.file_uploader("Upload equipment_usage.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "equipment_id": [f"EQUIP_{i}" for i in range(1, 31)],
            "equipment_type": np.random.choice(["Cardio", "Strength", "Stretch"], 30),
            "weekly_usage": np.random.randint(10, 200, 30)
        })

    st.subheader("📋 Equipment Usage")
    st.dataframe(df)

    df["priority"] = df["weekly_usage"] / df["weekly_usage"].max()
    df = df.sort_values("priority", ascending=False)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df["cleaning_day"] = [days[i % 7] for i in range(len(df))]

    st.subheader("🧽 Cleaning Schedule")
    st.dataframe(df[["equipment_id", "equipment_type", "weekly_usage", "cleaning_day"]])
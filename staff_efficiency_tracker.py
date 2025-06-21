import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🧑‍💼 Staff Efficiency Tracker")

    uploaded = st.file_uploader("Upload staff_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "staff_id": [f"S{i}" for i in range(100)],
            "role": np.random.choice(["Trainer", "Cleaner", "Reception"], 100),
            "zone": np.random.choice(["Turf", "Court", "Lobby", "Locker Room"], 100),
            "hours_logged": np.random.uniform(2, 8, 100).round(1),
            "tasks_completed": np.random.randint(2, 20, 100)
        })

    st.subheader("📋 Staff Logs")
    st.dataframe(df.head())

    df["efficiency"] = (df["tasks_completed"] / df["hours_logged"]).round(2)

    avg_eff = df.groupby("role")["efficiency"].mean().sort_values(ascending=False).reset_index()
    st.subheader("📊 Avg Efficiency by Role")
    st.dataframe(avg_eff)

    fig, ax = plt.subplots()
    avg_eff.set_index("role").plot(kind="bar", ax=ax, legend=False, color="mediumseagreen")
    ax.set_ylabel("Tasks per Hour")
    ax.set_title("Average Efficiency by Staff Role")
    st.pyplot(fig)
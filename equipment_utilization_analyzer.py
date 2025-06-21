import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("🏋️ Equipment Utilization Analyzer")

    uploaded = st.file_uploader("Upload equipment_usage.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        equipment = [f"Equip_{i}" for i in range(1, 21)]
        df = pd.DataFrame({
            "equipment_id": np.random.choice(equipment, 500),
            "usage_minutes": np.random.randint(10, 60, 500)
        })

    st.subheader("📋 Equipment Usage Logs")
    st.dataframe(df.head())

    usage_summary = df.groupby("equipment_id")["usage_minutes"].sum().sort_values(ascending=False)
    st.subheader("📈 Total Usage per Equipment")
    st.dataframe(usage_summary.reset_index())

    fig, ax = plt.subplots()
    usage_summary.plot(kind="bar", ax=ax, color="darkgreen")
    ax.set_ylabel("Total Minutes")
    ax.set_title("Equipment Utilization")
    st.pyplot(fig)

    threshold_high = usage_summary.quantile(0.9)
    threshold_low = usage_summary.quantile(0.1)

    st.subheader("⚠️ Overused Equipment")
    st.write(usage_summary[usage_summary > threshold_high])

    st.subheader("📉 Underused Equipment")
    st.write(usage_summary[usage_summary < threshold_low])
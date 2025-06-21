import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def run():
    st.title("📋 AI Operator Daily Briefing Generator")

    uploaded = st.file_uploader("Upload daily_metrics.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "metric": ["Check-ins", "New Signups", "Cancellations", "Incidents", "Cleaning Flags", "Revenue ($)"],
            "value": [np.random.randint(300, 800), np.random.randint(10, 50), np.random.randint(1, 10), np.random.randint(0, 5), np.random.randint(0, 4), np.random.randint(10000, 30000)]
        })

    st.subheader("📈 Today's Facility KPIs")
    st.dataframe(df)

    summary = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "key_points": [
            f"Total Check-ins: {df[df['metric'] == 'Check-ins']['value'].values[0]}",
            f"Revenue: ${df[df['metric'] == 'Revenue ($)']['value'].values[0]:,}",
            f"Incidents: {df[df['metric'] == 'Incidents']['value'].values[0]}",
            f"Cleaning Alerts: {df[df['metric'] == 'Cleaning Flags']['value'].values[0]}"
        ]
    }

    st.subheader("🧠 Briefing Summary")
    for point in summary["key_points"]:
        st.markdown(f"- {point}")
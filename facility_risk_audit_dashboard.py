import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("🧯 Facility Risk Audit Dashboard")

    uploaded = st.file_uploader("Upload risk_audit_zones.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "zone": ["Court", "Turf", "Track", "Locker Room", "Cafe", "Parking"],
            "violations": np.random.randint(0, 5, 6),
            "access_issues": np.random.randint(0, 3, 6),
            "incident_count": np.random.randint(0, 4, 6)
        })

    df["risk_score"] = (df["violations"] * 2 + df["access_issues"] + df["incident_count"] * 1.5).round(1)
    df["risk_level"] = pd.cut(df["risk_score"], bins=[-1, 2, 5, 10], labels=["Low", "Medium", "High"])

    st.subheader("📍 Zone Risk Assessment")
    st.dataframe(df)

    st.subheader("🔥 Risk Level Heatmap")
    fig, ax = plt.subplots()
    sns.barplot(x="zone", y="risk_score", hue="risk_level", data=df, ax=ax)
    ax.set_ylabel("Risk Score")
    st.pyplot(fig)
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("📊 Retention Cohort Comparison Dashboard")

    uploaded = st.file_uploader("Upload cohort_retention.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        cohorts = ["Jan", "Feb", "Mar", "Apr", "May"]
        df = pd.DataFrame({
            "cohort": np.repeat(cohorts, 6),
            "month": list(range(1, 7)) * 5,
            "retention_pct": np.random.uniform(0.2, 1.0, 30).round(2)
        })

    st.subheader("📋 Cohort Retention Data")
    st.dataframe(df.head())

    pivot = df.pivot(index="cohort", columns="month", values="retention_pct")
    st.subheader("🔥 Cohort Retention Heatmap")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(pivot, annot=True, fmt=".0%", cmap="YlGnBu", ax=ax)
    ax.set_title("Retention by Join Cohort")
    st.pyplot(fig)

    st.metric("Best Cohort", pivot.mean(axis=1).idxmax())
    st.metric("Worst Cohort", pivot.mean(axis=1).idxmin())
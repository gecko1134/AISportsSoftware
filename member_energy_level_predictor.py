import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("⚡ Member Energy Level Predictor")

    uploaded = st.file_uploader("Upload checkin_behavior.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(200)],
            "checkin_hour": np.random.choice(range(6, 22), 200),
            "weekday": np.random.randint(0, 7, 200)
        })

    st.subheader("📋 Check-In Behavior Logs")
    st.dataframe(df.head())

    df["period"] = pd.cut(df["checkin_hour"], bins=[0, 11, 17, 23], labels=["Morning", "Afternoon", "Evening"])
    preference = df.groupby(["member_id", "period"]).size().unstack().fillna(0)

    st.subheader("⚙️ Preferred Energy Period by Member")
    st.dataframe(preference.head())

    summary = preference.idxmax(axis=1).value_counts()
    st.subheader("⚡ Overall Energy Distribution")
    st.dataframe(summary)

    fig, ax = plt.subplots()
    summary.plot(kind="bar", color="mediumvioletred", ax=ax)
    ax.set_ylabel("Members")
    ax.set_title("Preferred Period for Activity")
    st.pyplot(fig)
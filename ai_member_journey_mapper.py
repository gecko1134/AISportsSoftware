import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def run():
    st.title("🧭 AI Member Journey Mapper")

    uploaded = st.file_uploader("Upload member_journey.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        stages = ["signup", "attend_class", "buy_addon", "refer_friend", "exit"]
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(200)],
            "num_classes": np.random.randint(0, 30, 200),
            "addons": np.random.randint(0, 5, 200),
            "referrals": np.random.randint(0, 3, 200),
            "active_months": np.random.randint(1, 24, 200),
            "exited": np.random.choice([0, 1], 200, p=[0.7, 0.3])
        })

    st.subheader("📋 Member Journey Data")
    st.dataframe(df.head())

    X = df[["num_classes", "addons", "referrals", "active_months", "exited"]]
    model = KMeans(n_clusters=4, random_state=42)
    df["journey_cluster"] = model.fit_predict(X)

    labels = {
        0: "Loyal Core",
        1: "Quick Exit",
        2: "Referral Drivers",
        3: "Infrequent Users"
    }
    df["journey_label"] = df["journey_cluster"].map(labels)

    st.subheader("🧬 Mapped Member Journeys")
    st.dataframe(df[["member_id", "journey_label"]])

    journey_counts = df["journey_label"].value_counts()
    fig, ax = plt.subplots()
    journey_counts.plot(kind="bar", ax=ax, color="purple")
    ax.set_ylabel("Members")
    ax.set_title("Distribution of Journey Types")
    st.pyplot(fig)
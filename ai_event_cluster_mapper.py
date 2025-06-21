import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def run():
    st.title("📊 AI Event Cluster Mapper")

    uploaded = st.file_uploader("Upload events.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "event_type": np.random.choice(["Tournament", "Open House", "Clinic"], 200),
            "expected_attendance": np.random.randint(50, 800, 200),
            "engagement_score": np.random.uniform(0.3, 1.0, 200)
        })

    st.subheader("📋 Event Data")
    st.dataframe(df.head())

    df["event_code"] = df["event_type"].astype("category").cat.codes
    X = df[["expected_attendance", "engagement_score", "event_code"]]

    model = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = model.fit_predict(X)

    st.subheader("🔍 Event Clusters")
    st.dataframe(df[["event_type", "expected_attendance", "engagement_score", "cluster"]].head(10))

    fig, ax = plt.subplots()
    scatter = ax.scatter(df["expected_attendance"], df["engagement_score"], c=df["cluster"], cmap="viridis", s=60)
    ax.set_xlabel("Expected Attendance")
    ax.set_ylabel("Engagement Score")
    ax.set_title("Event Clustering")
    st.pyplot(fig)
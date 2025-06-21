import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def run():
    st.title("📊 Facility Usage Pattern Clustering")

    uploaded = st.file_uploader("Upload checkin_logs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        from datetime import datetime, timedelta
        np.random.seed(42)
        df = pd.DataFrame({
            "user_id": [f"U{i}" for i in range(300)],
            "checkin_time": [datetime(2024, 6, 1) + timedelta(minutes=np.random.randint(6*60, 22*60)) for _ in range(300)],
            "zone": np.random.choice(["Gym", "Pool", "Track", "Studio"], 300)
        })

    df["checkin_time"] = pd.to_datetime(df["checkin_time"])
    df["hour"] = df["checkin_time"].dt.hour
    df["zone_code"] = df["zone"].astype("category").cat.codes

    df_group = df.groupby("user_id").agg({
        "hour": "mean",
        "zone_code": "mean",
        "checkin_time": "count"
    }).rename(columns={"checkin_time": "visits"}).reset_index()

    X = df_group[["hour", "zone_code", "visits"]]
    model = KMeans(n_clusters=3, random_state=42)
    df_group["cluster"] = model.fit_predict(X)

    st.subheader("📈 Cluster Summary")
    st.dataframe(df_group)

    fig, ax = plt.subplots()
    scatter = ax.scatter(df_group["hour"], df_group["visits"], c=df_group["cluster"], cmap="tab10", s=60)
    ax.set_xlabel("Avg Hour")
    ax.set_ylabel("Visits")
    ax.set_title("User Segmentation by Usage Pattern")
    st.pyplot(fig)
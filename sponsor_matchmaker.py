import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("🤝 Sponsor Matchmaker")

    uploaded = st.file_uploader("Upload sponsors.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("sponsors.csv")

    st.subheader("📋 Sponsor Data")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    df["sector_code"] = df["sector"].astype("category").cat.codes

    X = df[["spend", "engagement_score", "tier_code", "sector_code"]]

    # Fit k-means
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Cluster"] = kmeans.fit_predict(X)

    st.subheader("🔍 Matched Clusters")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="spend", y="engagement_score", hue="Cluster", style="tier", palette="tab10", ax=ax)
    st.pyplot(fig)

    st.subheader("📌 Suggestions")
    for c in df["Cluster"].unique():
        top = df[df["Cluster"] == c].sort_values("engagement_score", ascending=False).head(3)
        st.markdown(f"**Cluster {c} Matches:**")
        st.dataframe(top[["name", "tier", "sector", "spend", "engagement_score"]])
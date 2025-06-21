import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def run():
    st.title("🔗 Referral Chain Amplifier")

    uploaded = st.file_uploader("Upload member_referrals.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        members = [f"M{i}" for i in range(20)]
        referrals = pd.DataFrame({
            "referrer": np.random.choice(members, 40),
            "referred": [f"M{i}" for i in range(20, 60)]
        })

        df = referrals[referrals["referrer"] != referrals["referred"]]

    st.subheader("📋 Referral Data")
    st.dataframe(df.head())

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row["referrer"], row["referred"])

    st.subheader("📈 Referral Tree Visualization")
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=800, font_size=10, ax=ax)
    st.pyplot(fig)

    df_counts = pd.Series(dict(G.out_degree())).sort_values(ascending=False).reset_index()
    df_counts.columns = ["referrer", "referral_count"]

    st.subheader("🏆 Top Influencers by Referrals")
    st.dataframe(df_counts.head(10))
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("💸 Adaptive Dynamic Membership Pricing")

    uploaded = st.file_uploader("Upload membership_demand.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "tier": ["Silver", "Gold", "VIP"] * 12,
            "month": np.tile(range(1, 13), 3),
            "price": np.random.randint(40, 120, 36),
            "joins": np.random.randint(20, 200, 36),
            "churns": np.random.randint(5, 50, 36)
        })

    st.subheader("📋 Monthly Demand Data")
    st.dataframe(df.head())

    df["net_growth"] = df["joins"] - df["churns"]
    price_suggest = df.groupby("tier").apply(
        lambda d: d.sort_values("price").groupby("price")["net_growth"].mean().idxmax()
    ).reset_index(name="optimal_price")

    st.subheader("💰 Suggested Pricing Adjustments")
    st.dataframe(price_suggest)

    fig, ax = plt.subplots()
    for tier in df["tier"].unique():
        tier_df = df[df["tier"] == tier]
        ax.plot(tier_df["price"], tier_df["net_growth"], marker="o", label=tier)
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Net Growth")
    ax.set_title("Price Elasticity by Tier")
    ax.legend()
    st.pyplot(fig)
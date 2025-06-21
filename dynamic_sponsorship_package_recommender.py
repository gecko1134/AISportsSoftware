import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎯 Dynamic Sponsorship Package Recommender")

    uploaded = st.file_uploader("Upload sponsorship_inventory.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "asset": ["Turf Banner", "Scoreboard Logo", "App Ad", "Email Sponsor Slot", "Event Booth", "Kiosk Display"],
            "estimated_impressions": np.random.randint(500, 10000, 6),
            "cost": np.random.randint(300, 5000, 6)
        })

    st.subheader("📋 Sponsorship Inventory")
    st.dataframe(df)

    df["cost_per_impression"] = (df["cost"] / df["estimated_impressions"]).round(2)

    df_sorted = df.sort_values("cost_per_impression")
    tiers = {
        "Bronze": df_sorted.head(2),
        "Silver": df_sorted.iloc[2:4],
        "Gold": df_sorted.tail(2)
    }

    bundles = []
    for tier, items in tiers.items():
        bundle = {
            "tier": tier,
            "assets": list(items["asset"]),
            "total_cost": items["cost"].sum(),
            "total_impressions": items["estimated_impressions"].sum(),
            "avg_cpi": round(items["cost"].sum() / items["estimated_impressions"].sum(), 2)
        }
        bundles.append(bundle)

    bundles_df = pd.DataFrame(bundles)
    st.subheader("📦 Suggested Sponsorship Packages")
    st.dataframe(bundles_df)
import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🎯 Program Grant Opportunity Matcher")

    prog_file = st.file_uploader("Upload programs.csv", type=["csv"])
    grant_file = st.file_uploader("Upload grants.csv", type=["csv"])

    if prog_file and grant_file:
        programs = pd.read_csv(prog_file)
        grants = pd.read_csv(grant_file)
    else:
        np.random.seed(42)
        programs = pd.DataFrame({
            "program_id": [f"P{i}" for i in range(1, 6)],
            "name": ["Youth Fitness", "Senior Yoga", "Inclusive Sports", "Community Swim", "Adaptive Bootcamp"],
            "focus": ["Youth", "Seniors", "Disability", "Community", "Disability"]
        })

        grants = pd.DataFrame({
            "grant_id": [f"G{i}" for i in range(1, 6)],
            "title": ["Youth Activity Fund", "Senior Health Grant", "Inclusive Access Grant", "Neighborhood Wellness", "Adaptive Athletics Fund"],
            "focus": ["Youth", "Seniors", "Disability", "Community", "Disability"]
        })

    st.subheader("📋 Programs")
    st.dataframe(programs)

    st.subheader("💰 Available Grants")
    st.dataframe(grants)

    matched = []
    for _, p in programs.iterrows():
        for _, g in grants.iterrows():
            match_score = 1.0 if p["focus"] == g["focus"] else 0.0
            if match_score > 0:
                matched.append({
                    "program_id": p["program_id"],
                    "program_name": p["name"],
                    "grant_title": g["title"],
                    "focus": p["focus"],
                    "match_score": match_score
                })

    df_matched = pd.DataFrame(matched)
    st.subheader("✅ Matched Opportunities")
    st.dataframe(df_matched)
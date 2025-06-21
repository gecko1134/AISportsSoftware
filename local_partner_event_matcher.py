import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🤝 Local Partner Event Matcher")

    event_file = st.file_uploader("Upload events.csv", type=["csv"])
    partner_file = st.file_uploader("Upload partners.csv", type=["csv"])

    if event_file and partner_file:
        events = pd.read_csv(event_file)
        partners = pd.read_csv(partner_file)
    else:
        np.random.seed(42)
        events = pd.DataFrame({
            "event_id": [f"E{i}" for i in range(1, 6)],
            "event_name": ["Youth Sports Day", "Senior Wellness Fair", "Community Swim Gala", "School Field Day", "Adaptive Fitness Fest"],
            "focus": ["Youth", "Seniors", "Community", "Youth", "Disability"]
        })

        partners = pd.DataFrame({
            "partner_id": [f"P{i}" for i in range(1, 6)],
            "name": ["City Health Org", "High School League", "Senior Living Center", "YMCA", "Inclusive Play Org"],
            "focus": ["Community", "Youth", "Seniors", "Community", "Disability"]
        })

    st.subheader("📋 Events")
    st.dataframe(events)

    st.subheader("🏢 Community Partners")
    st.dataframe(partners)

    matched = []
    for _, event in events.iterrows():
        for _, partner in partners.iterrows():
            score = 1.0 if event["focus"] == partner["focus"] else 0.0
            if score:
                matched.append({
                    "event_id": event["event_id"],
                    "event_name": event["event_name"],
                    "partner_name": partner["name"],
                    "focus": event["focus"],
                    "match_score": score
                })

    result = pd.DataFrame(matched)
    st.subheader("✅ Matched Event-Partner Opportunities")
    st.dataframe(result)
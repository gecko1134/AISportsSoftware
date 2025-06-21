import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🤝 Smart Team Matchmaker AI")

    uploaded = st.file_uploader("Upload member_team_profiles.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(40)],
            "skill_level": np.random.choice(["Beginner", "Intermediate", "Advanced"], 40),
            "preferred_role": np.random.choice(["Captain", "Support", "Flexible"], 40),
            "available_days": np.random.choice(["MWF", "TTh", "Weekends"], 40)
        })

    df["team_id"] = (np.arange(len(df)) // 4) + 1
    df["team_tag"] = "Team " + df["team_id"].astype(str)

    st.subheader("🏷️ Suggested Teams")
    st.dataframe(df.sort_values("team_tag"))
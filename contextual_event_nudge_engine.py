import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📲 Contextual Event Nudge Engine")

    uploaded = st.file_uploader("Upload member_event_engagement.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(50)],
            "preferred_time": np.random.choice(["Morning", "Evening", "Weekend"], 50),
            "last_event_attended": np.random.choice(["Yoga Jam", "Bootcamp", "Spin Social"], 50),
            "interests": np.random.choice(["Fitness", "Social", "Wellness"], 50)
        })

    def suggest_event(row):
        if row["interests"] == "Fitness" and row["preferred_time"] == "Morning":
            return "🏋️ Join Sunrise Bootcamp!"
        elif row["interests"] == "Wellness":
            return "🧘 Try our Evening Stretch Flow"
        elif row["preferred_time"] == "Weekend":
            return "🎉 Weekend Social & Spin"
        else:
            return "💬 Join our community roundtable!"

    df["suggested_nudge"] = df.apply(suggest_event, axis=1)

    st.subheader("🎯 Personalized Event Nudges")
    st.dataframe(df[["member_id", "preferred_time", "interests", "suggested_nudge"]])
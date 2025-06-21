import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📅 AI Event Time Slot Optimizer")

    uploaded = st.file_uploader("Upload event_history.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_type": np.random.choice(["Game", "Workshop", "Fitness Class", "Expo"], 200),
            "weekday": np.random.randint(0, 7, 200),
            "hour": np.random.randint(8, 21, 200),
            "turnout": np.random.randint(10, 250, 200),
            "conflicts": np.random.randint(0, 5, 200)
        })

    st.subheader("📋 Historical Event Data")
    st.dataframe(df.head())

    df["score"] = df["turnout"] / (1 + df["conflicts"])
    optimal_slots = df.groupby(["weekday", "hour"])["score"].mean().unstack().fillna(0)

    st.subheader("⭐ Best Time Slot Scores (Higher = Better)")
    fig, ax = plt.subplots(figsize=(10, 4))
    optimal_slots.plot(kind="heatmap", cmap="YlGnBu", ax=ax)
    sns.heatmap(optimal_slots, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
    ax.set_title("Average Event Score by Day & Hour")
    st.pyplot(fig)

    best = df.groupby(["weekday", "hour"])["score"].mean().sort_values(ascending=False).reset_index().head(10)
    st.subheader("📌 Top Recommended Time Slots")
    st.dataframe(best)
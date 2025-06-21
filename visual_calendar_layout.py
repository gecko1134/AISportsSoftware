import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run():
    st.title("📅 Visual Calendar Layout")

    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    days = [start + timedelta(days=i) for i in range(7)]
    zones = ["Court 1", "Turf", "Studio", "Track"]

    df = pd.DataFrame({
        "event": np.random.choice(["Yoga", "Spin", "Game", "Training", "Camp"], 20),
        "zone": np.random.choice(zones, 20),
        "start_time": [start + timedelta(days=np.random.randint(0, 7), hours=np.random.randint(6, 21)) for _ in range(20)],
    })
    df["day"] = df["start_time"].dt.strftime("%A")
    df["hour"] = df["start_time"].dt.hour

    st.subheader("📋 Weekly Schedule Table")
    st.dataframe(df[["day", "hour", "event", "zone"]].sort_values(by=["day", "hour"]))

    selected_day = st.selectbox("Filter by Day", options=["All"] + sorted(df["day"].unique()))
    if selected_day != "All":
        df = df[df["day"] == selected_day]

    st.subheader("📊 Calendar View by Hour")
    st.dataframe(df.pivot_table(index="hour", columns="zone", values="event", aggfunc="first").fillna(""))
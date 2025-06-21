import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("📆 Booking Overlap Conflict Resolver")

    uploaded = st.file_uploader("Upload booking_schedule.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "booking_id": [f"B{i}" for i in range(100)],
            "zone": np.random.choice(["Court 1", "Turf A", "Studio", "Track"], 100),
            "start_hour": np.random.randint(6, 20, 100),
            "duration_hr": np.random.choice([1, 1.5, 2], 100)
        })

    df["end_hour"] = df["start_hour"] + df["duration_hr"]

    st.subheader("📋 Booking Schedule")
    st.dataframe(df.head())

    conflicts = []
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i < j and row1["zone"] == row2["zone"]:
                if row1["start_hour"] < row2["end_hour"] and row2["start_hour"] < row1["end_hour"]:
                    conflicts.append((row1["booking_id"], row2["booking_id"], row1["zone"]))

    conflict_df = pd.DataFrame(conflicts, columns=["Booking A", "Booking B", "Zone"])

    st.subheader("⚠️ Booking Conflicts Detected")
    st.dataframe(conflict_df)
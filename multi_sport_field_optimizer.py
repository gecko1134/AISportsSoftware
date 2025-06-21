import streamlit as st
import pandas as pd
import numpy as np

def run():
    st.title("🏟️ Multi-Sport Field Optimizer")

    uploaded = st.file_uploader("Upload field_schedule.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "booking_id": [f"B{i}" for i in range(20)],
            "sport": np.random.choice(["Soccer", "Lacrosse", "Flag Football", "Ultimate Frisbee"], 20),
            "players": np.random.randint(10, 40, 20),
            "duration_hr": np.random.choice([1, 1.5, 2], 20),
            "requested_zone": np.random.choice(["Turf A", "Turf B", "Full Field"], 20)
        })

    st.subheader("📋 Requested Field Bookings")
    st.dataframe(df)

    zone_capacity = {"Turf A": 25, "Turf B": 25, "Full Field": 60}
    df["zone_feasible"] = df.apply(lambda row: any(row["players"] <= cap for zone, cap in zone_capacity.items() if row["requested_zone"] in zone or row["requested_zone"] == "Full Field"), axis=1)
    df["assigned_zone"] = df.apply(
        lambda row: row["requested_zone"] if row["zone_feasible"] else (
            "Turf A" if row["players"] <= zone_capacity["Turf A"] else (
                "Turf B" if row["players"] <= zone_capacity["Turf B"] else "Split Time Slot"
            )
        ),
        axis=1
    )

    st.subheader("📐 Zone Assignment Recommendations")
    st.dataframe(df[["booking_id", "sport", "players", "requested_zone", "assigned_zone"]])
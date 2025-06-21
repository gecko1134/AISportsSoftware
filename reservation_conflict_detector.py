import streamlit as st
import pandas as pd

def run():
    st.title("📅 Reservation Conflict Detector")

    uploaded = st.file_uploader("Upload bookings.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("bookings.csv")

    st.subheader("📋 Booking Data")
    st.dataframe(df.head())

    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
    df = df.sort_values(["facility_id", "datetime"])

    conflicts = []
    for fid in df["facility_id"].unique():
        subset = df[df["facility_id"] == fid].sort_values("datetime")
        for i in range(1, len(subset)):
            prev = subset.iloc[i - 1]
            curr = subset.iloc[i]
            prev_end = prev["datetime"] + pd.to_timedelta(prev["duration"], unit="m")
            if curr["datetime"] < prev_end:
                conflicts.append({
                    "facility_id": fid,
                    "conflict_1": f"{prev['member_id']} at {prev['datetime']}",
                    "conflict_2": f"{curr['member_id']} at {curr['datetime']}"
                })

    if conflicts:
        conflict_df = pd.DataFrame(conflicts)
        st.subheader("⚠️ Detected Conflicts")
        st.dataframe(conflict_df)
    else:
        st.success("✅ No conflicts detected!")
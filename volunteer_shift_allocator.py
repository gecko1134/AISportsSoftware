import streamlit as st
import pandas as pd

def run():
    st.title("🙌 Volunteer Shift Allocator")

    vol_file = st.file_uploader("Upload volunteers.csv", type=["csv"])
    shift_file = st.file_uploader("Upload shifts.csv", type=["csv"])

    if vol_file and shift_file:
        vols = pd.read_csv(vol_file)
        shifts = pd.read_csv(shift_file)

        st.subheader("📋 Volunteers")
        st.dataframe(vols.head())

        st.subheader("📅 Shifts")
        st.dataframe(shifts.head())

        assignments = []
        for _, shift in shifts.iterrows():
            available = vols[
                (vols["available_day"] == shift["day"]) &
                (vols["available_time"] == shift["time"])
            ]
            if not available.empty:
                v = available.sample(1).iloc[0]
                assignments.append({
                    "shift_id": shift["shift_id"],
                    "day": shift["day"],
                    "time": shift["time"],
                    "role": shift["role"],
                    "volunteer": v["name"]
                })
                vols = vols[vols["name"] != v["name"]]

        df_out = pd.DataFrame(assignments)
        st.subheader("✅ Assigned Shifts")
        st.dataframe(df_out)

        st.download_button("📥 Download Schedule CSV", df_out.to_csv(index=False), "volunteer_schedule.csv", "text/csv")
    else:
        st.info("Upload both volunteers.csv and shifts.csv to generate assignments.")
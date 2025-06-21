import streamlit as st
import pandas as pd
from datetime import timedelta

def run():
    st.title("📋 Coach Schedule Efficiency Analyzer")

    uploaded = st.file_uploader("Upload coach_schedule.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "coach": ["Coach A"] * 3 + ["Coach B"] * 3,
            "date": ["2024-06-10"] * 6,
            "start_time": ["09:00", "11:00", "13:00", "08:00", "08:30", "12:00"],
            "end_time": ["10:00", "12:00", "14:00", "09:00", "11:00", "13:00"]
        })

    st.subheader("📋 Schedule Data")
    st.dataframe(df)

    df["start_time"] = pd.to_datetime(df["date"] + " " + df["start_time"])
    df["end_time"] = pd.to_datetime(df["date"] + " " + df["end_time"])
    df = df.sort_values(["coach", "start_time"])

    summary = []
    for coach in df["coach"].unique():
        cdf = df[df["coach"] == coach]
        total_time = cdf["end_time"].sub(cdf["start_time"]).sum()
        gaps = timedelta()
        for i in range(1, len(cdf)):
            gap = cdf.iloc[i]["start_time"] - cdf.iloc[i - 1]["end_time"]
            if gap.total_seconds() > 0:
                gaps += gap
        efficiency = total_time / (total_time + gaps) if total_time + gaps > timedelta() else 0
        summary.append({
            "coach": coach,
            "sessions": len(cdf),
            "total_hours": total_time.total_seconds() / 3600,
            "gap_hours": gaps.total_seconds() / 3600,
            "efficiency": round(efficiency * 100, 1)
        })

    st.subheader("⚖️ Efficiency Summary")
    st.dataframe(pd.DataFrame(summary))
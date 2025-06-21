import streamlit as st
import pandas as pd

def run():
    st.title("🧑‍⚖️ Referee Match Scheduler")

    st.write("Upload game schedule and ref availability to auto-assign matches.")

    game_file = st.file_uploader("Upload games.csv", type=["csv"])
    ref_file = st.file_uploader("Upload referees.csv", type=["csv"])

    if game_file and ref_file:
        games = pd.read_csv(game_file)
        refs = pd.read_csv(ref_file)

        st.subheader("📋 Games")
        st.dataframe(games.head())

        st.subheader("🧾 Referees")
        st.dataframe(refs.head())

        # Match refs by sport and availability (same date & time)
        assigned = []
        for _, game in games.iterrows():
            candidates = refs[
                (refs["sport"] == game["sport"]) &
                (refs["date"] == game["date"]) &
                (refs["time"] == game["time"])
            ]
            if not candidates.empty:
                ref = candidates.sample(1).iloc[0]
                assigned.append({
                    "game_id": game["game_id"],
                    "date": game["date"],
                    "time": game["time"],
                    "sport": game["sport"],
                    "referee": ref["name"]
                })
                refs = refs[refs["name"] != ref["name"]]  # remove assigned ref

        result_df = pd.DataFrame(assigned)
        st.subheader("✅ Match Assignments")
        st.dataframe(result_df)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Assignments CSV", csv, "ref_schedule.csv", "text/csv")
    else:
        st.info("Please upload both game and referee CSV files.")
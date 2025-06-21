import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📆 Seasonal Program Demand Shift Analyzer")

    uploaded = st.file_uploader("Upload seasonal_program_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        programs = ["Yoga", "Swim", "Soccer", "Weights", "Zumba"]
        df = pd.DataFrame({
            "season": np.tile(["Spring", "Summer", "Fall", "Winter"], 25),
            "program": np.repeat(programs, 20),
            "participants": np.random.randint(20, 300, 100)
        })

    st.subheader("📋 Program Participation by Season")
    st.dataframe(df.head())

    shift = df.groupby(["program", "season"])["participants"].mean().unstack().fillna(0)
    st.subheader("📈 Seasonal Participation Trends")
    st.dataframe(shift.round())

    fig, ax = plt.subplots()
    shift.T.plot(ax=ax)
    ax.set_title("Seasonal Trends by Program")
    ax.set_ylabel("Avg Participants")
    st.pyplot(fig)
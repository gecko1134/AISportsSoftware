import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run():
    st.title("📊 Event Overbooking Risk Visualizer")

    uploaded = st.file_uploader("Upload event_registrations.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "event_id": [f"E{i}" for i in range(50)],
            "event_type": np.random.choice(["Swim Meet", "Yoga Class", "Basketball Game"], 50),
            "capacity": np.random.randint(30, 200, 50),
            "registrations": np.random.randint(20, 250, 50),
            "hour": np.random.choice(range(6, 22), 50)
        })

    df["risk_flag"] = df["registrations"] > df["capacity"]
    st.subheader("📋 Event Registration Overview")
    st.dataframe(df)

    st.subheader("⚠️ Overbooking Risk Events")
    st.dataframe(df[df["risk_flag"]][["event_id", "event_type", "capacity", "registrations", "hour"]])

    fig, ax = plt.subplots()
    ax.scatter(df["capacity"], df["registrations"], c=df["risk_flag"].map({True: "red", False: "green"}))
    ax.plot([0, 250], [0, 250], linestyle="--", color="gray")
    ax.set_xlabel("Capacity")
    ax.set_ylabel("Registrations")
    ax.set_title("Event Capacity vs. Signups")
    st.pyplot(fig)
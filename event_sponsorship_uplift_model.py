import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def run():
    st.title("📈 Event Sponsorship Uplift Model")

    uploaded = st.file_uploader("Upload sponsored_events.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "event_id": range(1, 101),
            "sponsored": np.random.choice([0, 1], 100, p=[0.5, 0.5]),
            "base_attendance": np.random.randint(100, 500, 100),
            "exposure_score": np.random.uniform(0.3, 1.0, 100),
            "revenue": np.random.randint(3000, 15000, 100)
        })
        df["uplifted_attendance"] = df["base_attendance"] + df["sponsored"] * np.random.randint(50, 150, 100)

    st.subheader("📋 Event Data")
    st.dataframe(df.head())

    X = df[["sponsored", "base_attendance", "exposure_score"]]
    y = df["uplifted_attendance"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    uplift = model.coef_[0]

    st.subheader("📊 Sponsor Uplift Estimate")
    st.metric("Predicted Sponsor Uplift", f"{uplift:.2f} attendees")

    df["predicted"] = model.predict(X)

    fig, ax = plt.subplots()
    ax.scatter(df["base_attendance"], df["uplifted_attendance"], label="Actual", alpha=0.6)
    ax.scatter(df["base_attendance"], df["predicted"], label="Predicted", alpha=0.6)
    ax.set_xlabel("Base Attendance")
    ax.set_ylabel("Uplifted Attendance")
    ax.set_title("Sponsor Uplift Modeling")
    ax.legend()
    st.pyplot(fig)
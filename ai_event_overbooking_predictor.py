import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("📈 Event Overbooking Predictor")

    uploaded = st.file_uploader("Upload event_signups.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "event_id": range(1, 101),
            "venue_capacity": np.random.randint(100, 500, 100),
            "signups": np.random.randint(80, 600, 100),
            "day_of_week": np.random.randint(0, 7, 100),
            "overbooked": np.random.choice([0, 1], 100, p=[0.8, 0.2])
        })

    st.subheader("📋 Event Signup Data")
    st.dataframe(df.head())

    X = df[["venue_capacity", "signups", "day_of_week"]]
    y = df["overbooked"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Overbooking Risk Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["risk_score"] = model.predict_proba(X)[:, 1]
    risky = df[df["risk_score"] > 0.6]

    st.subheader("⚠️ High-Risk Events")
    st.dataframe(risky[["event_id", "signups", "venue_capacity", "risk_score"]])
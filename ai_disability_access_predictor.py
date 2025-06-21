import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("♿ Disability Access Predictor")

    uploaded = st.file_uploader("Upload program_enrollments.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "participant_id": [f"P{i}" for i in range(100)],
            "age": np.random.randint(6, 75, 100),
            "program_type": np.random.choice(["Yoga", "Swim", "Basketball", "Fitness"], 100),
            "previous_notes": np.random.choice([0, 1], 100, p=[0.7, 0.3]),
            "access_requested": np.random.choice([0, 1], 100, p=[0.8, 0.2])
        })

    st.subheader("📋 Enrollment Data")
    st.dataframe(df.head())

    df["program_code"] = df["program_type"].astype("category").cat.codes
    X = df[["age", "program_code", "previous_notes"]]
    y = df["access_requested"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Accessibility Request Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["risk_score"] = model.predict_proba(X)[:, 1]
    flags = df[df["risk_score"] > 0.6]

    st.subheader("🔍 Participants Likely Needing Access Support")
    st.dataframe(flags[["participant_id", "program_type", "risk_score"]])
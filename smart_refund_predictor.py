import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("💸 Smart Refund Predictor")

    uploaded = st.file_uploader("Upload refund_requests.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "program_type": np.random.choice(["Camp", "League", "Drop-in"], 150),
            "days_before_event": np.random.randint(0, 30, 150),
            "reason_code": np.random.choice([0, 1, 2], 150),  # 0=Scheduling, 1=Illness, 2=Other
            "refunded": np.random.choice([0, 1], 150, p=[0.6, 0.4])
        })

    st.subheader("📋 Refund Request Data")
    st.dataframe(df.head())

    df["program_code"] = df["program_type"].astype("category").cat.codes
    X = df[["days_before_event", "reason_code", "program_code"]]
    y = df["refunded"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Refund Likelihood Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    st.metric("Overall Refund Rate", f"{100 * y.mean():.1f}%")
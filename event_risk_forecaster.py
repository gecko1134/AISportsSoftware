import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("⚠️ Event Risk Forecaster")

    uploaded = st.file_uploader("Upload events.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("events.csv")

    st.subheader("📋 Events Data")
    st.dataframe(df.head())

    df["weather_code"] = df["weather"].map({"Sunny": 0, "Cloudy": 1, "Rain": 2})
    df["sport_code"] = df["sport"].astype("category").cat.codes
    df["risk_flag"] = (df["expected_attendance"] > 400) | (df["weather"] == "Rain")

    X = df[["sport_code", "weather_code", "expected_attendance"]]
    y = df["risk_flag"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Risk Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    st.metric("High-Risk Event %", f"{100 * y.mean():.1f}%")
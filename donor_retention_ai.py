import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def run():
    st.title("🔁 Donor Retention Predictor")

    uploaded = st.file_uploader("Upload donor_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("donor_data.csv")

    st.subheader("📋 Donor Data")
    st.dataframe(df.head())

    df["days_since_donation"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["last_donation"])).dt.days
    df["tier_code"] = df["tier"].astype("category").cat.codes
    df["freq_code"] = df["frequency"].astype("category").cat.codes

    X = df[["donation_total", "days_since_donation", "tier_code", "freq_code"]]
    y = df["churned"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    report = classification_report(y_test, preds, output_dict=True)

    st.subheader("📈 Prediction Results")
    st.json(report)

    st.metric("Churn Rate", f"{100 * y.mean():.1f}%")
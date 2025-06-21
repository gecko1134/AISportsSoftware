import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("📆 Sponsor Renewal Predictor")

    uploaded = st.file_uploader("Upload sponsors.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "tier": np.random.choice(["Bronze", "Silver", "Gold"], 100),
            "spend": np.random.randint(5000, 30000, 100),
            "engagement_score": np.random.uniform(0.5, 1.0, 100),
            "tenure_months": np.random.randint(1, 36, 100),
            "renewed": np.random.choice([0, 1], 100, p=[0.3, 0.7])
        })

    st.subheader("📋 Sponsor Data")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    X = df[["spend", "engagement_score", "tenure_months", "tier_code"]]
    y = df["renewed"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Renewal Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    st.metric("Renewal Rate", f"{100 * y.mean():.1f}%")
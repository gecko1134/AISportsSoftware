import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("📑 Grant Success Forecaster")

    uploaded = st.file_uploader("Upload grant_applications.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "program": np.random.choice(["Youth Sports", "Community Health", "Facility Expansion"], 200),
            "amount": np.random.randint(5000, 50000, 200),
            "sector": np.random.choice(["Government", "Foundation", "Corporate"], 200),
            "prior_award": np.random.choice([0, 1], 200, p=[0.7, 0.3]),
            "won": np.random.choice([0, 1], 200, p=[0.6, 0.4])
        })

    st.subheader("📋 Grant Application Data")
    st.dataframe(df.head())

    df["program_code"] = df["program"].astype("category").cat.codes
    df["sector_code"] = df["sector"].astype("category").cat.codes

    X = df[["amount", "prior_award", "program_code", "sector_code"]]
    y = df["won"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    report = classification_report(y_test, preds, output_dict=True)

    st.subheader("📊 Grant Success Prediction Report")
    st.json(report)

    st.metric("Overall Win Rate", f"{100 * y.mean():.1f}%")
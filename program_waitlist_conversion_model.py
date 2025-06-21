import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("📋 Program Waitlist Conversion Model")

    uploaded = st.file_uploader("Upload waitlist_data.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "user_id": [f"U{i}" for i in range(100)],
            "program": np.random.choice(["Yoga", "Swim", "Basketball"], 100),
            "days_waiting": np.random.randint(1, 20, 100),
            "prior_signups": np.random.randint(0, 5, 100),
            "converted": np.random.choice([0, 1], 100, p=[0.7, 0.3])
        })

    st.subheader("📋 Waitlist Data")
    st.dataframe(df.head())

    df["program_code"] = df["program"].astype("category").cat.codes
    X = df[["program_code", "days_waiting", "prior_signups"]]
    y = df["converted"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Conversion Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["conversion_score"] = model.predict_proba(X)[:, 1]
    top = df.sort_values("conversion_score", ascending=False).head(10)

    st.subheader("✅ Top Conversion Candidates")
    st.dataframe(top[["user_id", "program", "conversion_score"]])
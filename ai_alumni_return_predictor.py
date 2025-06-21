import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🔄 AI Alumni Return Predictor")

    uploaded = st.file_uploader("Upload alumni_members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "alumni_id": [f"A{i}" for i in range(100)],
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "total_visits": np.random.randint(5, 80, 100),
            "exit_reason_code": np.random.choice([0, 1, 2], 100),  # 0=moved, 1=price, 2=other
            "time_since_exit_days": np.random.randint(30, 900, 100),
            "rejoined": np.random.choice([0, 1], 100, p=[0.75, 0.25])
        })

    st.subheader("📋 Alumni Data")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes
    X = df[["tier_code", "total_visits", "exit_reason_code", "time_since_exit_days"]]
    y = df["rejoined"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Return Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["return_likelihood"] = model.predict_proba(X)[:, 1]
    top_returners = df.sort_values("return_likelihood", ascending=False).head(10)

    st.subheader("🔁 High Likelihood Returnees")
    st.dataframe(top_returners[["alumni_id", "return_likelihood"]])
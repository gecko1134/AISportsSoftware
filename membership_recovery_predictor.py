import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🔄 Membership Recovery Predictor")

    uploaded = st.file_uploader("Upload lapsed_members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"L{i}" for i in range(100)],
            "tenure_months": np.random.randint(1, 36, 100),
            "avg_sessions_per_month": np.random.uniform(1, 12, 100),
            "last_feedback_score": np.random.uniform(2.0, 5.0, 100),
            "rejoined": np.random.choice([0, 1], 100, p=[0.7, 0.3])
        })

    st.subheader("📋 Lapsed Member Profiles")
    st.dataframe(df.head())

    X = df[["tenure_months", "avg_sessions_per_month", "last_feedback_score"]]
    y = df["rejoined"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Rejoin Probability Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["rejoin_score"] = model.predict_proba(X)[:, 1]
    st.subheader("📈 Top Rejoin Candidates")
    st.dataframe(df[["member_id", "rejoin_score"]].sort_values("rejoin_score", ascending=False).head(10))
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🚀 Program Launch Success Predictor")

    uploaded = st.file_uploader("Upload program_launches.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "program_type": np.random.choice(["Yoga", "Weights", "Bootcamp"], 100),
            "instructor_rating": np.random.uniform(3.0, 5.0, 100),
            "marketing_spend": np.random.randint(100, 2000, 100),
            "season": np.random.choice(["Winter", "Spring", "Summer", "Fall"], 100),
            "successful": np.random.choice([0, 1], 100, p=[0.3, 0.7])
        })

    st.subheader("📋 Launch History")
    st.dataframe(df.head())

    df["type_code"] = df["program_type"].astype("category").cat.codes
    df["season_code"] = df["season"].astype("category").cat.codes
    X = df[["type_code", "instructor_rating", "marketing_spend", "season_code"]]
    y = df["successful"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Launch Success Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["success_prob"] = model.predict_proba(X)[:, 1]
    st.subheader("🎯 Predicted Success Scores")
    st.dataframe(df[["program_type", "season", "success_prob"]].sort_values("success_prob", ascending=False).head(10))
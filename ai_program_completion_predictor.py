import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run():
    st.title("🎓 AI Program Completion Predictor")

    uploaded = st.file_uploader("Upload program_enrollments.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": [f"M{i}" for i in range(100)],
            "program_type": np.random.choice(["Yoga", "Weights", "Swim"], 100),
            "sessions_attended": np.random.randint(0, 12, 100),
            "total_sessions": np.random.randint(5, 12, 100),
            "engagement_score": np.random.uniform(2.0, 5.0, 100),
            "completed": np.random.choice([0, 1], 100, p=[0.4, 0.6])
        })

    st.subheader("📋 Enrollment History")
    st.dataframe(df.head())

    df["type_code"] = df["program_type"].astype("category").cat.codes
    df["attendance_ratio"] = df["sessions_attended"] / df["total_sessions"]
    X = df[["type_code", "attendance_ratio", "engagement_score"]]
    y = df["completed"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Completion Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["completion_score"] = model.predict_proba(X)[:, 1]
    st.subheader("✅ Predicted Completion Scores")
    st.dataframe(df[["member_id", "program_type", "completion_score"]].sort_values("completion_score", ascending=False).head(10))
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("👶 Child Program Uplift Predictor")

    uploaded = st.file_uploader("Upload youth_programs.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "age": np.random.randint(6, 16, 300),
            "sessions_attended": np.random.randint(1, 20, 300),
            "coach_rating": np.random.uniform(3.0, 5.0, 300).round(1),
            "tier": np.random.choice(["Standard", "Advanced", "Elite"], 300),
            "uplift": np.random.choice([0, 1], 300, p=[0.3, 0.7])
        })

    st.subheader("📋 Youth Program Data")
    st.dataframe(df.head())

    df["tier_code"] = df["tier"].astype("category").cat.codes

    X = df[["age", "sessions_attended", "coach_rating", "tier_code"]]
    y = df["uplift"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📈 Uplift Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    st.metric("Uplift Rate", f"{100 * y.mean():.1f}%")
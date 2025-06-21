import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("📈 Event Conversion Predictor")

    uploaded = st.file_uploader("Upload event_attendance.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "event_type": np.random.choice(["Open House", "Tournament", "Clinic"], 300),
            "sport": np.random.choice(["Soccer", "Basketball", "Pickleball"], 300),
            "attended": np.random.choice([1], 300),
            "age": np.random.randint(12, 60, 300),
            "converted_to_member": np.random.choice([0, 1], 300, p=[0.7, 0.3])
        })

    st.subheader("📋 Attendance Data")
    st.dataframe(df.head())

    df["event_code"] = df["event_type"].astype("category").cat.codes
    df["sport_code"] = df["sport"].astype("category").cat.codes

    X = df[["event_code", "sport_code", "age"]]
    y = df["converted_to_member"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Conversion Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    st.metric("Conversion Rate", f"{100 * y.mean():.1f}%")
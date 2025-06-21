import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("📉 Membership Downgrade Predictor")

    uploaded = st.file_uploader("Upload members.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        import numpy as np
        import datetime
        np.random.seed(42)
        df = pd.DataFrame({
            "member_id": range(1000, 1100),
            "tier": np.random.choice(["Silver", "Gold", "VIP"], 100),
            "age": np.random.randint(18, 65, 100),
            "last_visit": [datetime.date(2024, 1, 1) + datetime.timedelta(days=np.random.randint(0, 90)) for _ in range(100)],
            "downgraded": np.random.choice([0, 1], 100, p=[0.8, 0.2])
        })

    df["days_since_last"] = (pd.to_datetime("2024-06-01") - pd.to_datetime(df["last_visit"])).dt.days
    df["tier_code"] = df["tier"].astype("category").cat.codes

    X = df[["age", "days_since_last", "tier_code"]]
    y = df["downgraded"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Downgrade Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    st.metric("Downgrade Risk Rate", f"{100 * y.mean():.1f}%")
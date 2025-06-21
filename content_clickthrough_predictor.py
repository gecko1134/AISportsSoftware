import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def run():
    st.title("📨 Content Clickthrough Predictor")

    uploaded = st.file_uploader("Upload content_interactions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "campaign_id": [f"C{i}" for i in range(150)],
            "segment": np.random.choice(["Youth", "Adults", "Seniors"], 150),
            "content_type": np.random.choice(["Tips", "Promo", "Event"], 150),
            "hour_sent": np.random.randint(8, 22, 150),
            "clicked": np.random.choice([0, 1], 150, p=[0.7, 0.3])
        })

    st.subheader("📋 Content Campaign Data")
    st.dataframe(df.head())

    df["segment_code"] = df["segment"].astype("category").cat.codes
    df["type_code"] = df["content_type"].astype("category").cat.codes
    X = df[["segment_code", "type_code", "hour_sent"]]
    y = df["clicked"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    st.subheader("📊 Clickthrough Prediction Report")
    report = classification_report(y_test, preds, output_dict=True)
    st.json(report)

    df["predicted_ctr"] = model.predict_proba(X)[:, 1]
    top_items = df.sort_values("predicted_ctr", ascending=False).head(10)

    st.subheader("📈 Top Predicted Campaigns")
    st.dataframe(top_items[["campaign_id", "segment", "content_type", "predicted_ctr"]])
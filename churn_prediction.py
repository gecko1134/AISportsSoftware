
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

class ChurnPredictor:
    def __init__(self, model_path=None):
        if model_path:
            self.model, self.scaler = joblib.load(model_path)
        else:
            self.model = LogisticRegression(max_iter=200)
            self.scaler = StandardScaler()

    def train(self, df, features, target):
        X = df[features]
        y = df[target]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        joblib.dump((self.model, self.scaler), "churn_model.pkl")

    def predict(self, df):
        X_scaled = self.scaler.transform(df)
        return self.model.predict_proba(X_scaled)[:, 1]

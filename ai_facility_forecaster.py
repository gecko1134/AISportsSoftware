
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib

class FacilityForecaster:
    def __init__(self):
        self.model = GradientBoostingRegressor()
        self.scaler = StandardScaler()

    def train(self, df, features, target):
        X = df[features]
        y = df[target]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        joblib.dump((self.model, self.scaler), "facility_forecast_model.pkl")

    def predict(self, df):
        X_scaled = self.scaler.transform(df)
        return self.model.predict(X_scaled)

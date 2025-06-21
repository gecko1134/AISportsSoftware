# SPORTAI SuperSuite – AI Enhanced (Top 15 Modules)

This is the full AI-enhanced release of the SPORTAI platform, now featuring 15 fully functional real-time AI modules.

## ✅ What's Included

- 📈 AI forecasts, scoring, and predictions
- 📊 Real-time charts, metrics, and outputs
- 📁 CSV loaders and synthetic demo data support
- 📦 Fully structured Streamlit app with sidebar navigation

## 🔧 Key Modules

- `ai_event_forecast` – predict attendance
- `ai_scheduler_tool` – optimize facility time slots
- `ai_revenue_maximizer` – model pricing vs. profit
- `churn_prediction` – flag members likely to leave
- `sponsor_matchmaker` – match sponsors to programs
- `contract_builder` – auto-generate agreements
- `ai_member_ranker` – score engagement
- `donor_retention_ai` – predict donor churn
- `usage_heatmap_gen` – visualize busy hours
- `ai_waitlist_optimizer` – suggest open slots
- `league_revenue_splitter` – model league ROI
- `member_lifecycle_predictor` – segment by tenure
- `facility_energy_predictor` – estimate usage costs
- `event_risk_forecaster` – weather/overbooking risk

## ▶️ Run Locally

```bash
pip install streamlit scikit-learn matplotlib seaborn
streamlit run main_app.py
```

## 📁 Folder Layout

```bash
.
├── main_app.py
├── modules/
│   ├── ai_event_forecast.py
│   ├── ...
│   └── event_risk_forecaster.py
```

## 🌐 Deploy to Streamlit Cloud

1. Push this folder to GitHub
2. Visit https://streamlit.io/cloud
3. Deploy `main_app.py`
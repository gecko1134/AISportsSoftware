# 🚀 Deployment Guide: SPORTAI Suite

## 🔁 1. Push to GitHub

### ✅ Create Repo
- Go to https://github.com/new
- Name: `SPORTAI_Suite`
- No README or .gitignore
- Create repository

### 💻 Push Locally
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/SPORTAI_Suite.git
git add .
git commit -m "Initial deployable version"
git branch -M main
git push -u origin main
```

---

## 🌐 2. Deploy to Streamlit Cloud

### 🪄 Launch Your App
1. Go to https://streamlit.io/cloud
2. Click "New App" and select your `SPORTAI_Suite` repo
3. App file: `run_sportai.py`
4. Environment: auto-reads from `requirements.txt`
5. Click **Deploy**

---

## 🔐 3. Optional: Add API Keys

Create a file `.streamlit/secrets.toml` with:
```toml
openai_key = "sk-..."
mapbox_token = "..."
email_password = "..."
```

---

## 🧪 4. Run Locally (Dev Mode)

Install dependencies:
```bash
pip install -r requirements.txt
```

Then launch:
```bash
python run_sportai.py
```
Or directly:
```bash
streamlit run main_app.py
```
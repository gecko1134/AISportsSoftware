import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

def run():
    st.title("🌍 Multi-Language Support AI")

    uploaded = st.file_uploader("Upload facility_texts.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        df = pd.DataFrame({
            "label": ["Welcome", "Hours", "Rules", "Emergency Exit", "Childcare"],
            "english_text": [
                "Welcome to the Sports Complex!",
                "Open daily 6 AM - 10 PM",
                "No outside food or drinks allowed",
                "Follow signs to nearest exit",
                "Available Mon–Fri 8 AM–1 PM"
            ]
        })

    lang = st.selectbox("Translate to", ["Spanish", "French", "German", "Chinese", "Arabic"])
    st.subheader(f"🌐 Translated Content: {lang}")

    df[f"{lang}_translation"] = df["english_text"].apply(lambda x: GoogleTranslator(source='auto', target=lang.lower()).translate(x))
    st.dataframe(df)
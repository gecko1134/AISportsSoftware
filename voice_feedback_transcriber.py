import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import tempfile

def run():
    st.title("🎙️ Voice Feedback Transcriber")

    uploaded_audio = st.file_uploader("Upload voice memo (.wav)", type=["wav"])
    if uploaded_audio:
        st.audio(uploaded_audio)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_audio.read())
            tmp_path = tmp.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                st.subheader("📝 Transcribed Text")
                st.write(text)

                sentiment = TextBlob(text).sentiment
                st.subheader("🔍 Sentiment Analysis")
                st.json({
                    "polarity": round(sentiment.polarity, 2),
                    "subjectivity": round(sentiment.subjectivity, 2)
                })

            except sr.UnknownValueError:
                st.error("Could not understand the audio.")
            except sr.RequestError:
                st.error("Speech recognition service error.")
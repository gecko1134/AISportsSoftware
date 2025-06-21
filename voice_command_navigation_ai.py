import streamlit as st
import speech_recognition as sr
import tempfile

def run():
    st.title("🎙️ Voice Command Navigation AI")

    uploaded = st.file_uploader("Upload a voice command (.wav)", type=["wav"])
    if uploaded:
        st.audio(uploaded)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded.read())
            audio_path = tmp.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio).lower()
            st.subheader("🗣️ Detected Command")
            st.write(text)

            if "schedule" in text or "class" in text:
                response = "📅 The full class schedule is available from 6 AM to 10 PM daily."
            elif "yoga" in text:
                response = "🧘 Yoga classes run at 7 AM and 6 PM."
            elif "court" in text:
                response = "🏀 Courts are open from 8 AM to 9 PM. Booking required."
            else:
                response = "🤖 I didn't catch that. Try asking about a class or time."

            st.subheader("💬 Assistant Response")
            st.write(response)
        except:
            st.error("Voice command not understood.")
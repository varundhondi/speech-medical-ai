from faster_whisper import WhisperModel
import streamlit as st


# Load model ONLY once
@st.cache_resource
def load_model():
    model = WhisperModel("base", compute_type="int8")
    return model


def transcribe_audio(audio_path):

    model = load_model()
    segments, _ = model.transcribe(audio_path)
    transcript = " ".join([seg.text for seg in segments])
    return transcript
import streamlit as st
from pyannote.audio import Pipeline
import whisper

token = st.secrets["HUGGINGFACE_TOKEN"]

@st.cache_resource
def load_diarization():
    return Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=token
    )


pipeline = load_diarization()

# Get token from Streamlit secrets
token = st.secrets["HUGGINGFACE_TOKEN"]

# Load Whisper model
@st.cache_resource
def load_whisper():
    return whisper.load_model("tiny")

whisper_model = load_whisper()


# Load diarization model
@st.cache_resource
def load_diarization():
    return Pipeline.from_pretrained(
        "pyannote/speaker-diarization",
        use_auth_token=token
    )

pipeline = load_diarization()


def diarize_conversation(audio_path):

    diarization = pipeline(audio_path)

    transcript = whisper_model.transcribe(audio_path)

    segments = transcript["segments"]

    conversation = []

    speaker_toggle = ["👨‍⚕️ Doctor", "🧑 Patient"]
    speaker_index = 0

    for seg in segments:

        text = seg["text"].strip()

        speaker = speaker_toggle[speaker_index % 2]

        conversation.append(f"{speaker}: {text}")

        speaker_index += 1

    return "\n\n".join(conversation)
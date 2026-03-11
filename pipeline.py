from diarization import diarize_conversation
from symptom_extractor import extract_symptoms
from code_predictor import predict_icd, predict_cpt


def process_audio(audio_path):

    transcript = diarize_conversation(audio_path)

    symptoms = extract_symptoms(transcript)

    icd_results = {}
    cpt_results = {}

    for symptom in symptoms:

        icd_results[symptom] = predict_icd(symptom)
        cpt_results[symptom] = predict_cpt(symptom)

    return transcript, symptoms, icd_results, cpt_results
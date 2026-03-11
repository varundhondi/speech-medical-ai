import spacy

nlp = spacy.load("en_core_web_sm")

medical_keywords = [
    "pain",
    "dizziness",
    "nausea",
    "vomiting",
    "fever",
    "cough",
    "headache",
    "indigestion",
    "stomach pain"
]

def extract_symptoms(text):

    symptoms = []

    text = text.lower()

    for word in medical_keywords:
        if word in text:
            symptoms.append(word)

    return list(set(symptoms))
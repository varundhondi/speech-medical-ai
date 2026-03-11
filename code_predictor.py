import pandas as pd
from fuzzywuzzy import process
import streamlit as st


# =========================
# Load datasets
# =========================
@st.cache_data
def load_data():
    icd = pd.read_excel("data/icd11.xlsx")
    cpt = pd.read_excel("data/cpt_codes.xlsx")
    return icd, cpt

icd, cpt = load_data()


# =========================
# Clean ICD dataset
# =========================

# Ensure correct datatype
icd["Title"] = icd["Title"].astype(str)

# Remove dashed hierarchy markers from ICD titles
icd["Title"] = icd["Title"].str.replace("-", "", regex=False)

# Remove extra whitespace
icd["Title"] = icd["Title"].str.strip()

# Lowercase for matching
icd["Title"] = icd["Title"].str.lower()


# =========================
# Clean CPT dataset
# =========================

# Keep only first two columns
cpt = cpt.iloc[:, :2]

# Rename columns
cpt.columns = ["Code", "Description"]

# Remove empty rows
cpt = cpt.dropna()

# Ensure string datatype
cpt["Description"] = cpt["Description"].astype(str)

# Lowercase descriptions
cpt["Description"] = cpt["Description"].str.lower()

# Remove extra spaces
cpt["Description"] = cpt["Description"].str.strip()


# =========================
# ICD Prediction
# =========================

def predict_icd(symptom, top_n=5):

    symptom = symptom.lower()

    matches = process.extract(symptom, icd["Title"], limit=top_n)

    results = []

    for desc, score, _ in matches:

        # Skip weak matches
        if score < 70:
            continue

        row = icd[icd["Title"] == desc].iloc[0]

        results.append({
            "Code": row["Code"],
            "Title": row["Title"],
            "Confidence": score
        })

    return results


# =========================
# CPT Prediction
# =========================

def predict_cpt(symptom, top_n=5):

    symptom = symptom.lower()

    matches = process.extract(symptom, cpt["Description"], limit=top_n)

    results = []

    for desc, score, _ in matches:

        # Skip weak matches
        if score < 55:
            continue

        row = cpt[cpt["Description"] == desc].iloc[0]

        results.append({
            "Code": row["Code"],
            "Description": row["Description"],
            "Confidence": score
        })

    return results
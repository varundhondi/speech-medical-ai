import pandas as pd


def generate_analytics(symptoms, icd, cpt):

    data = []

    for s in symptoms:

        diagnosis = icd[s][0]["Title"] if icd[s] else "Unknown"
        procedure = cpt[s][0]["Description"] if cpt[s] else "Unknown"

        data.append({
            "Symptom": s,
            "Diagnosis": diagnosis,
            "Procedure": procedure
        })

    df = pd.DataFrame(data)

    return df
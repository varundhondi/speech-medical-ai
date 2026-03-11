import streamlit as st
import pandas as pd
from pipeline import process_audio
import plotly.express as px
import plotly.graph_objects as go
import tempfile

st.set_page_config(
    page_title="AI Medical Coding Assistant",
    page_icon="🩺",
    layout="wide"
)

# Title
st.title("🩺 AI Medical Coding Assistant")
st.markdown("### 🧠 Speech → Diagnosis → ICD / CPT Codes")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ System Controls")

uploaded_file = st.sidebar.file_uploader(
    "🎤 Upload Doctor-Patient Audio",
    type=["wav", "mp3"]
)

st.sidebar.markdown("---")
st.sidebar.info(
"""
📌 This AI system performs:

• Speech to Text  
• Symptom Detection  
• ICD-11 Code Prediction  
• CPT Procedure Prediction  
• Diagnosis Assistance  
"""
)

# SESSION STATE (PREVENT PIPELINE RERUNS)
if "results" not in st.session_state:
    st.session_state.results = None

# AUDIO SAVE
import tempfile

# AUDIO SAVE (deployment-safe)
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

# PROCESS BUTTON
if uploaded_file and st.button("🚀 Process Audio"):

    with st.spinner("Processing medical conversation..."):

        transcript, symptoms, icd, cpt = process_audio(audio_path)

        st.session_state.results = {
            "transcript": transcript,
            "symptoms": symptoms,
            "icd": icd,
            "cpt": cpt
        }

# LOAD RESULTS
results = st.session_state.results

if results:

    transcript = results["transcript"]
    symptoms = results["symptoms"]
    icd = results["icd"]
    cpt = results["cpt"]

    st.success("✅ Audio processed successfully")

    # Extract diagnoses
    diagnosis_list = []

    for s in symptoms:
        if icd[s]:
            diagnosis_list.append(icd[s][0]["Title"])

    top_diagnosis = diagnosis_list[0] if diagnosis_list else "Unknown"

    # ======================
    # Patient Case Summary
    # ======================

    st.markdown("## 🏥 Patient Case Summary")

    st.markdown(
    f"""
    <div style="background:#0f172a;padding:20px;border-radius:12px;margin-bottom:20px">

    ### 🧑 Patient Overview

    **Symptoms Detected:** {", ".join(symptoms)}

    **Primary Diagnosis:** {top_diagnosis}

    **Recommended Tests:** {", ".join([cpt[s][0]["Description"] for s in symptoms if cpt[s]])}

    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown("---")

    # ======================
    # Transcript
    # ======================

    st.markdown("## 🗣 Doctor–Patient Conversation")

    for line in transcript.split("\n\n"):

        if "Doctor" in line:
            st.markdown(
                f"<div style='background:#1e293b;padding:12px;border-radius:10px;margin-bottom:8px'>{line}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background:#065f46;padding:12px;border-radius:10px;margin-bottom:8px'>{line}</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ======================
    # Symptoms
    # ======================

    st.header("🤒 Detected Patient Symptoms")

    if symptoms:
        for s in symptoms:
            st.markdown(f"• **{s.capitalize()}**")
    else:
        st.warning("No symptoms detected")

    st.markdown("---")

    # ======================
    # ICD / CPT Codes
    # ======================

    col1, col2 = st.columns(2)

    # ICD
    with col1:

        st.header("📋 ICD-11 Diagnosis Codes")

        for symptom in symptoms:

            st.subheader(f"Symptom: {symptom}")

            df = pd.DataFrame(icd[symptom])

            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No ICD match found")

    # CPT
    with col2:

        st.header("💉 CPT Procedure Codes")

        for symptom in symptoms:

            st.subheader(f"Symptom: {symptom}")

            df = pd.DataFrame(cpt[symptom])

            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No CPT match found")

    st.markdown("---")

    # ======================
    # Diagnosis Confidence
    # ======================

    st.subheader("📊 Diagnosis Confidence")

    for symptom in symptoms:

        df = pd.DataFrame(icd[symptom])

        if not df.empty:

            fig = px.bar(
                df,
                x="Title",
                y="Confidence",
                title=f"Diagnosis Probability for {symptom}",
                color="Confidence"
            )

            fig.update_layout(template="plotly_dark")

            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ======================
    # Suggested Diagnosis
    # ======================

    st.header("🧾 Suggested Diagnosis")

    if diagnosis_list:

        for d in diagnosis_list:
            st.markdown(f"🩺 **{d.capitalize()}**")

    else:
        st.warning("Diagnosis could not be determined")

    st.markdown("---")

    # ======================
    # Case Summary
    # ======================

    st.header("📑 Case Summary")

    summary = f"""
Patient Symptoms:
{", ".join(symptoms)}

Possible Diagnoses:
{", ".join(diagnosis_list)}
"""

    st.text_area("Clinical Summary", summary, height=150)

    st.markdown("---")

    # ======================
    # Clinical Decision Support
    # ======================

    st.markdown("## 🧠 Clinical Decision Support")

    for s in symptoms:

        if icd[s]:

            diagnosis = icd[s][0]["Title"]
            confidence = icd[s][0]["Confidence"]

            st.markdown(
            f"""
            🔎 **Symptom:** {s}

            🩺 **Possible Condition:** {diagnosis}

            📊 **AI Confidence:** {confidence}%
            """
            )

    # ======================
    # Clinical Decision Flow
    # ======================

    st.markdown("## 🧠 Clinical Decision Flow")

    for symptom in symptoms:

        if icd[symptom]:

            diagnosis = icd[symptom][0]["Title"]
            icd_code = icd[symptom][0]["Code"]

            procedure = "None"

            if cpt[symptom]:
                procedure = cpt[symptom][0]["Description"]

            labels = [symptom, diagnosis, icd_code, procedure]

            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=20,
                    thickness=30,
                    label=labels
                ),
                link=dict(
                    source=[0,1,2],
                    target=[1,2,3],
                    value=[1,1,1]
                )
            )])

            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ======================
    # Analytics
    # ======================

    st.header("📊 Medical Analytics")

    analytics_df = pd.DataFrame({
        "Symptom": symptoms,
        "Diagnosis": diagnosis_list,
        "Procedure": [cpt[s][0]["Description"] if cpt[s] else "N/A" for s in symptoms]
    })

    fig1 = px.bar(
        analytics_df,
        x="Symptom",
        color="Symptom",
        title="🩺 Detected Symptoms Distribution"
    )

    fig1.update_layout(template="plotly_dark")

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        analytics_df,
        x="Diagnosis",
        color="Diagnosis",
        title="🧠 Predicted Diagnoses"
    )

    fig2.update_layout(template="plotly_dark")

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.bar(
        analytics_df,
        x="Procedure",
        color="Procedure",
        title="💉 Recommended Procedures"
    )

    fig3.update_layout(template="plotly_dark")

    st.plotly_chart(fig3, use_container_width=True)

    # ======================
    # Severity
    # ======================

    st.markdown("## 🚨 Severity Assessment")

    severity_keywords = ["vomiting","dizziness","chest pain","bleeding"]

    severity = "Low"

    for s in symptoms:
        if s in severity_keywords:
            severity = "Moderate"

    if severity == "Moderate":
        st.warning("⚠️ Moderate severity symptoms detected. Further examination recommended.")
    else:
        st.success("✅ Symptoms appear non-critical.")

    st.markdown("---")

    # ======================
    # Download Report
    # ======================

    st.download_button(
        label="📥 Download Medical Report",
        data=summary,
        file_name="patient_report.txt",
        mime="text/plain"
    )

else:
    st.info("👈 Upload a doctor-patient audio file and click **Process Audio** to start analysis")
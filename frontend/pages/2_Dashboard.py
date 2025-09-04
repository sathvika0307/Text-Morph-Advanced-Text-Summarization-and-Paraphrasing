import sys
import os
import streamlit as st
import textstat
import matplotlib.pyplot as plt
import docx
import PyPDF2
from backend.utils import verify_jwt, add_logout_button
from database.user_db import save_uploaded_file


# Add project root to sys.path so imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ---------- LOGIN CHECK ----------
token = st.session_state.get("jwt_token")
username = verify_jwt(token)

if not username:
    st.warning("⚠ Please login to access the dashboard.")
    # Use session_state to trigger safe rerun
    if 'redirect_trigger' not in st.session_state:
        st.session_state.redirect_trigger = True
    else:
        st.session_state.redirect_trigger = not st.session_state.redirect_trigger
    st.stop()

# ---------- PAGE ----------
st.title("📊 Document Readability Dashboard")
add_logout_button()

# ---------- COLUMNS WITH SPACING ----------
col_left, col_spacer, col_right = st.columns([5, 1, 5])

with col_left:
    uploaded_file = st.file_uploader("Upload a document:", type=["txt", "pdf", "docx"])
    content = None
    
    if uploaded_file:
        # Save file in DB
        file_bytes = uploaded_file.read()
        save_uploaded_file(username, file_bytes)
        st.success("📄 File uploaded and saved in the database successfully!")

        # Decode content for readability
        if uploaded_file.type == "text/plain":
            content = file_bytes.decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            content = "".join([page.extract_text() for page in pdf_reader.pages])
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            doc = docx.Document(uploaded_file)
            content = "\n".join([para.text for para in doc.paragraphs])

        if content:
            # ---------- READABILITY SCORES ----------
            fk = textstat.flesch_kincaid_grade(content)
            gf = textstat.gunning_fog(content)
            smog = textstat.smog_index(content)
            num_words = len(content.split())
            if num_words < 50:
                smog = min(smog, (fk + gf)/2)

            st.subheader("Readability Scores 📊")
            st.write(f"**Flesch-Kincaid Grade:** {fk:.2f}")
            st.write(f"**Gunning Fog Index:** {gf:.2f}")
            st.write(f"**SMOG Index:** {smog:.2f}")

with col_right:
    if content:
        # ---------- OVERALL DIFFICULTY ----------
        avg_score = (fk + gf + smog)/3
        if avg_score <= 4:
            overall_cat = "Beginner"
        elif avg_score <= 8:
            overall_cat = "Intermediate"
        else:
            overall_cat = "Advanced"
        st.markdown(f"### 🏷️ Overall Difficulty Level: **{overall_cat}**")

        # ---------- BAR GRAPH ----------
        raw_values = [fk, gf, smog]
        labels = ["Flesch-Kincaid", "Gunning Fog", "SMOG"]
        colors = ["green" if x <= 4 else "orange" if x <= 8 else "red" for x in raw_values]

        fig, ax = plt.subplots(figsize=(5,4))
        bars = ax.bar(labels, raw_values, color=colors, width=0.5)
        ax.set_ylim(0, max(raw_values)*1.1)
        ax.set_ylabel("Readability Score")
        ax.set_title("Document Readability Graph")

        for bar, val in zip(bars, raw_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + (max(raw_values)*0.02), f"{val:.2f}",
                    ha='center', fontsize=10, fontweight='bold')

        st.pyplot(fig)

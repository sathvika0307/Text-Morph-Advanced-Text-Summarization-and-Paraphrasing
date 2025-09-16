import sys
import os
import re
import streamlit as st
import docx
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
from rouge_score import rouge_scorer

# Add backend folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.text_readability import calculate_readability
from backend.utils import verify_jwt, add_logout_button
from backend.summarization import summarize_text
from backend.paraphrasing import generate_paraphrase  # New version
from database.user_db import save_uploaded_file, save_processed_text

# ---------- LOGIN CHECK ----------
token = st.session_state.get("jwt_token")
username = verify_jwt(token)
if not username:
    st.warning("⚠ Please login to access the dashboard.")
    st.stop()

# ---------- HELPER FUNCTIONS ----------
def clean_text(text: str) -> str:
    text = re.sub(r"(?:<|&lt;)[nN](?:>|&gt;)", " ", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def word_count(text: str) -> int:
    return len(text.split())

def compression_percentage(original: str, generated: str) -> float:
    orig_len = word_count(original)
    gen_len = word_count(generated)
    if orig_len == 0:
        return 0.0
    return round((1 - gen_len / orig_len) * 100, 2)

def calculate_rouge(reference: str, generated: str) -> dict:
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return {k: v.fmeasure for k, v in scores.items()}

def plot_rouge_bar(rouge_scores: dict):
    metrics = list(rouge_scores.keys())
    values = [rouge_scores[m] for m in metrics]
    colors = ["green" if v > 0.5 else "orange" if v > 0.3 else "red" for v in values]

    fig, ax = plt.subplots(figsize=(5, 3))
    bars = ax.bar(metrics, values, color=colors, width=0.5)
    ax.set_ylim(0, 1)
    ax.set_ylabel("F1 Score")
    ax.set_title("ROUGE Scores")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.02, f"{val:.2f}", ha='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

# ---------- PAGE ----------
st.title("📊 AI-Text-Morph Dashboard")
add_logout_button()

st.markdown("### 📄 Input your document or paste text here")

# 1️⃣ Upload file
with st.expander("Upload your document", expanded=False):
    uploaded_file = st.file_uploader("Choose a file (txt, pdf, docx):", type=["txt", "pdf", "docx"])

# 2️⃣ Paste text
pasted_text = st.text_area("Or paste your text here:", height=400, placeholder="Paste your document text here...")

content = None
file_name = "pasted_text.txt"

# ---------- READ FILE ----------
if uploaded_file:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    save_uploaded_file(username, file_bytes, file_name)
    st.success("📄 File uploaded successfully!")
    try:
        if uploaded_file.type == "text/plain":
            content = file_bytes.decode("utf-8", errors="ignore")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            content = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            doc = docx.Document(uploaded_file)
            content = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
elif pasted_text.strip():
    content = pasted_text
    file_name = "pasted_text.txt"

# ---------- CLEAN TEXT ----------
if content:
    content = clean_text(content)
    st.success("✅ Text ready for processing!")

    task = st.radio("Select Task:", ["Readability", "Summarization", "Paraphrasing"])

    # ---------------- READABILITY ----------------
    if task == "Readability":
        scores, overall, chart_data = calculate_readability(content)
        st.subheader("Readability Scores 📊")
        for k, v in scores.items():
            st.write(f"{k}: **{v:.2f}**")
        st.markdown(f"### 🏷️ Overall Difficulty: *{overall}*")

        try:
            st.pyplot(chart_data)
        except AttributeError:
            if isinstance(chart_data, pd.DataFrame):
                st.bar_chart(chart_data)
            elif isinstance(chart_data, dict):
                df_chart = pd.DataFrame(list(chart_data.items()), columns=["Metric","Score"]).set_index("Metric")
                st.bar_chart(df_chart)

    # ---------------- SUMMARIZATION ----------------
    elif task == "Summarization":
        length_option = st.selectbox("Select Summary Length:", ["Short", "Medium", "Long"])
        summary_length_map = {"Short":"short", "Medium":"medium", "Long":"long"}

        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary, _ = summarize_text(content, summary_length=summary_length_map[length_option])
                summary = clean_text(summary)
                save_processed_text(username, "summary", content, summary, "pegasus")

                rouge_scores = calculate_rouge(content, summary)
                compression = compression_percentage(content, summary)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Original Text")
                    st.text_area("Original", content, height=400)
                with col2:
                    st.subheader("Summary")
                    st.text_area("Summary", summary, height=400)

                st.subheader("ROUGE Scores 📊")
                plot_rouge_bar(rouge_scores)

                st.markdown(f"*Original Words:* {word_count(content)}  |  *Summary Words:* {word_count(summary)}  |  *Compression:* {compression}%")

    # ---------------- PARAPHRASING ----------------
    elif task == "Paraphrasing":
        complexity_option = st.selectbox("Select Paraphrase Complexity:", ["Basic","Medium","Advanced"])
        complexity_map = {"Basic":"basic","Medium":"medium","Advanced":"advanced"}

        if st.button("Generate Paraphrase"):
            with st.spinner("Paraphrasing..."):
                # Use new generate_paraphrase (google/pegasus-xsum)
                para_text = generate_paraphrase(content, complexity=complexity_map[complexity_option])
                para_text = clean_text(para_text)
                save_processed_text(username, "paraphrase", content, para_text, "pegasus")

                rouge_scores = calculate_rouge(content, para_text)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Original Text")
                    st.text_area("Original", content, height=400)
                with col2:
                    st.subheader("Paraphrased Text")
                    st.text_area("Paraphrase", para_text, height=400)

                st.subheader("ROUGE Scores 📊")
                plot_rouge_bar(rouge_scores)

                st.markdown(f"*Original Words:* {word_count(content)}  |  *Paraphrased Words:* {word_count(para_text)}")

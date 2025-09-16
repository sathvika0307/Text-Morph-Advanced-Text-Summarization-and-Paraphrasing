"""
Summarization module using HuggingFace Pegasus.
Handles long documents safely with configurable summary lengths.
Returns summary along with ROUGE-1, ROUGE-2, and ROUGE-L scores.
"""

import logging
from typing import Dict, Tuple
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

try:
    from rouge_score import rouge_scorer
except ImportError:
    rouge_scorer = None

# Cache loaded model/tokenizer
_pegasus_cache: Dict[str, Tuple[AutoTokenizer, AutoModelForSeq2SeqLM, torch.device]] = {}

def clean_generated_text(text: str) -> str:
    """Remove unwanted <n> tokens and extra spaces."""
    import re
    text = re.sub(r"(?:<|&lt;)[nN](?:>|&gt;)", " ", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def summarize_text(text: str, model_name: str = "google/pegasus-xsum", summary_length: str = "medium") -> Tuple[str, Dict[str, float]]:
    text = (text or "").strip()
    if not text:
        return "", {}

    # Load model/tokenizer (cached)
    if model_name not in _pegasus_cache:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            _pegasus_cache[model_name] = (tokenizer, model, device)
        except Exception as e:
            logging.exception(f"Failed to load Pegasus model: {e}")
            return "", {}

    tokenizer, model, device = _pegasus_cache[model_name]

    # Token length settings
    length_map = {"short": (30, 80), "medium": (80, 120), "long": (120, 300)}
    min_len, max_len = length_map.get(summary_length, (80, 120))

    # Split long texts into chunks
    words = text.split()
    chunks = [" ".join(words[i:i + 800]) for i in range(0, len(words), 800)]

    chunk_summaries = []
    for chunk in chunks:
        try:
            inputs = tokenizer(chunk, truncation=True, padding="longest", return_tensors="pt", max_length=1024)
            for k, v in inputs.items():
                inputs[k] = v.to(device)

            output_ids = model.generate(
                inputs["input_ids"],
                max_length=max_len,
                min_length=min_len,
                num_beams=6,
                length_penalty=2.0,
                early_stopping=True
            )
            summary_chunk = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            chunk_summaries.append(clean_generated_text(summary_chunk))
        except Exception as e:
            logging.warning(f"Chunk summarization failed: {e}")

    if not chunk_summaries:
        return "", {}

    # Combine chunk summaries
    if len(chunk_summaries) == 1:
        summary = chunk_summaries[0]
    else:
        combined = " ".join(chunk_summaries)
        try:
            inputs = tokenizer(combined, truncation=True, padding="longest", return_tensors="pt", max_length=1024)
            for k, v in inputs.items():
                inputs[k] = v.to(device)

            output_ids = model.generate(
                inputs["input_ids"],
                max_length=max_len,
                min_length=max(min_len, 20),
                num_beams=6,
                length_penalty=2.0,
                early_stopping=True
            )
            summary = clean_generated_text(tokenizer.decode(output_ids[0], skip_special_tokens=True))
        except Exception as e:
            logging.warning(f"Final summarization failed: {e}")
            summary = " ".join(chunk_summaries)

    # ---------- Compute ROUGE ----------
    rouge_scores = {}
    if rouge_scorer:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(text, summary)
        rouge_scores = {k: v.fmeasure for k, v in scores.items()}

    return summary, rouge_scores

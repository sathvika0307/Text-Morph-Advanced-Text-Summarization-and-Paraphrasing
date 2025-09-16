"""
Paraphrasing module using HuggingFace Pegasus (google/pegasus-xsum).
Rephrases text while keeping original meaning, with adjustable complexity.
Does NOT use NLTK, so avoids punkt issues.
"""

import re
from typing import Dict, Tuple
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Cache model & tokenizer
_model_cache: Dict[str, Tuple[AutoTokenizer, AutoModelForSeq2SeqLM]] = {}

def load_model(model_name: str = "google/pegasus-xsum"):
    """Load and cache Pegasus model + tokenizer."""
    if model_name not in _model_cache:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        _model_cache[model_name] = (tokenizer, model)
    return _model_cache[model_name]

def split_into_sentences(text: str) -> list:
    """Split text into sentences using regex (avoiding NLTK)."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

def generate_paraphrase(text: str, complexity: str = "medium") -> str:
    """Paraphrase input text with adjustable complexity."""
    tokenizer, model = load_model()

    # Complexity → decoding params
    decoding_map = {
        "basic": dict(num_beams=3, max_length=60, do_sample=True, temperature=0.7),
        "medium": dict(num_beams=5, max_length=80, do_sample=True, temperature=0.9),
        "advanced": dict(num_beams=8, max_length=100, do_sample=True, temperature=1.0),
    }
    params = decoding_map.get(complexity, decoding_map["medium"])

    sentences = split_into_sentences(text)
    if not sentences:
        return text

    paraphrased_sentences = []
    for sent in sentences:
        batch = tokenizer([sent], truncation=True, padding="longest", return_tensors="pt")
        outputs = model.generate(**batch, **params)
        out = tokenizer.decode(outputs[0], skip_special_tokens=True)
        out = re.sub(r"\.\.+$", ".", out).strip()  # Clean trailing dots
        paraphrased_sentences.append(out)

    return " ".join(paraphrased_sentences)

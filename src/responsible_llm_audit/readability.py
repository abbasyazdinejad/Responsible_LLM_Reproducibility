"""Readability metrics.

A self-contained, rule-based Flesch--Kincaid Grade Level (FKGL) is used so the
pipeline runs fully offline (no external corpus such as NLTK cmudict is required).
Computed on the ``display`` text form.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from .config import Config

_WORD = re.compile(r"[A-Za-z']+")
_VOWELS = re.compile(r"[aeiouy]+")
_SENT = re.compile(r"[.!?]+")


def sentence_count(text: str) -> int:
    return sum(1 for p in _SENT.split(str(text)) if p.strip()) or 1


def syllables(word: str) -> int:
    """Rule-based syllable estimate (consecutive vowels; silent trailing 'e')."""
    w = word.lower()
    if not w:
        return 0
    s = len(_VOWELS.findall(w))
    if w.endswith("e") and s > 1:
        s -= 1
    return max(1, s)


def flesch_kincaid_grade(text: str) -> float:
    if not isinstance(text, str) or not text.strip():
        return np.nan
    words = _WORD.findall(text)
    n_words = max(1, len(words))
    n_sent = sentence_count(text)
    n_syll = sum(syllables(w) for w in words)
    return 0.39 * (n_words / n_sent) + 11.8 * (n_syll / n_words) - 15.59


def flesch_reading_ease(text: str) -> float:
    if not isinstance(text, str) or not text.strip():
        return np.nan
    words = _WORD.findall(text)
    n_words = max(1, len(words))
    n_sent = sentence_count(text)
    n_syll = sum(syllables(w) for w in words)
    return 206.835 - 1.015 * (n_words / n_sent) - 84.6 * (n_syll / n_words)


def avg_sentence_length(text: str) -> float:
    parts = [len(p.split()) for p in _SENT.split(str(text)) if p.strip()]
    return float(np.mean(parts)) if parts else np.nan


def chars_per_word(text: str) -> float:
    ws = _WORD.findall(str(text))
    return float(np.mean([len(w) for w in ws])) if ws else np.nan


def readability_by_model(resp: pd.DataFrame, cfg: Config, text_col: str = "display") -> pd.DataFrame:
    """Per-model readability summary computed on ``text_col``.

    Columns: ``model, avg_sentence_len_words, avg_chars_per_word, fkgl_mean, fkgl_sd``.
    """
    tmp = resp.copy()
    tmp["_sl"] = tmp[text_col].map(avg_sentence_length)
    tmp["_cw"] = tmp[text_col].map(chars_per_word)
    tmp["_fk"] = tmp[text_col].map(flesch_kincaid_grade)
    rows = []
    for tag in cfg.model_tags:
        g = tmp[tmp["model"] == tag]
        rows.append({
            "model": cfg.model_labels[tag],
            "avg_sentence_len_words": round(g["_sl"].mean(), 3),
            "avg_chars_per_word": round(g["_cw"].mean(), 3),
            "fkgl_mean": round(g["_fk"].mean(), 2),
            "fkgl_sd": round(g["_fk"].std(), 2),
        })
    return pd.DataFrame(rows)

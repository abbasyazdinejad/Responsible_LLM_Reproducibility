"""Response cleaning and the two analytical text forms.

Two distinct text forms are produced from each raw model response:

* ``full_cleaned``  -- reasoning traces removed, NOT word-trimmed. Used for the
  safety/cultural content markers (which concern whether the model *provided* the
  guidance at all) and for the trimming sensitivity analysis.
* ``display``       -- the full-cleaned text trimmed to a 180-word display cap. Used
  for readability, response-length, and keyword-framing metrics.
"""
from __future__ import annotations

import re

import pandas as pd

from .config import Config

_THINK_BLOCK = re.compile(r"<think>.*?</think>", flags=re.DOTALL | re.IGNORECASE)
_THINK_TAG = re.compile(r"</?think>", flags=re.IGNORECASE)
_WS = re.compile(r"\s+")


def strip_reasoning_traces(text: object) -> str:
    """Remove non-user-facing ``<think>`` reasoning traces and collapse whitespace."""
    if not isinstance(text, str):
        return ""
    text = _THINK_BLOCK.sub("", text)
    text = _THINK_TAG.sub("", text)
    return _WS.sub(" ", text).strip()


def trim_to_words(text: str, max_words: int) -> str:
    """Trim ``text`` to at most ``max_words`` whitespace-delimited tokens."""
    return " ".join(text.split()[:max_words])


def add_text_forms(resp: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """Return a copy of ``resp`` with cleaning columns added.

    Adds: ``had_think_raw``, ``full_cleaned``, ``full_words``, ``display``,
    ``display_words``, ``trimmed_at_cap``.
    """
    if "response" not in resp.columns:
        raise ValueError("resp must contain a 'response' column.")
    cap = cfg.display_word_cap
    out = resp.copy()
    out["had_think_raw"] = out["response"].astype(str).str.lower().str.contains("<think")
    out["full_cleaned"] = out["response"].map(strip_reasoning_traces)
    out["full_words"] = out["full_cleaned"].map(lambda t: len(t.split()))
    out["display"] = out["full_cleaned"].map(lambda t: trim_to_words(t, cap))
    out["display_words"] = out["display"].map(lambda t: len(t.split()))
    out["trimmed_at_cap"] = out["full_words"] >= cap
    return out

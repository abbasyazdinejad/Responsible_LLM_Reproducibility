"""Safety and cultural marker detection (lexical, keyword-based).

Markers are lexical indicators, not judgements of contextual adequacy. Primary
reporting uses the ``full_cleaned`` text form (see :mod:`preprocessing`).
"""
from __future__ import annotations

import re
from typing import Dict

import pandas as pd

from .config import Config


def compile_patterns(cfg: Config) -> Dict[str, re.Pattern]:
    """Compile the marker regular expressions from ``config/marker_patterns.json``."""
    return {name: re.compile(pat, re.IGNORECASE) for name, pat in cfg.marker_patterns.items()}


def add_marker_flags(resp: pd.DataFrame, cfg: Config, text_col: str = "full_cleaned") -> pd.DataFrame:
    """Add boolean marker columns (``marker_crisis`` etc.) computed on ``text_col``."""
    if text_col not in resp.columns:
        raise ValueError(f"resp has no column '{text_col}'.")
    pats = compile_patterns(cfg)
    out = resp.copy()
    for name, pat in pats.items():
        out[f"marker_{name}"] = out[text_col].fillna("").str.contains(pat)
    return out


def marker_rates(resp: pd.DataFrame, cfg: Config, text_col: str = "full_cleaned") -> pd.DataFrame:
    """Return per-model marker prevalence (proportion of responses) on ``text_col``.

    Columns: ``model, cultural_marker_rate, crisis_guidance_rate,
    disclaimer_or_referral_rate``.
    """
    flagged = add_marker_flags(resp, cfg, text_col=text_col)
    rows = []
    for tag in cfg.model_tags:
        g = flagged[flagged["model"] == tag]
        rows.append({
            "model": cfg.model_labels[tag],
            "cultural_marker_rate": round(g["marker_cultural"].mean(), 3),
            "crisis_guidance_rate": round(g["marker_crisis"].mean(), 3),
            "disclaimer_or_referral_rate": round(g["marker_disclaimer"].mean(), 3),
        })
    return pd.DataFrame(rows)

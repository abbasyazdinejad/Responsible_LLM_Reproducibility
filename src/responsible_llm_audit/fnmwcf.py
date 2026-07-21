"""FNMWCF lexical coverage (a transparent proxy; not a measure of cultural adequacy).

Uses the published theme lexicon in ``config/fnmwcf_lexicon.json``. A theme is counted
as present in a response if any of its terms appears. Computed on the ``display`` form.
"""
from __future__ import annotations

from typing import List

import pandas as pd

from .config import Config


def theme_present(text: str, terms: List[str]) -> bool:
    t = str(text).lower()
    return any(term in t for term in terms)


def coverage_by_model(resp: pd.DataFrame, cfg: Config, text_col: str = "display") -> pd.DataFrame:
    """Per-model, per-theme lexical coverage (% of responses containing >=1 term).

    Columns: ``model``, one ``cov_<theme>`` column per theme, and ``mean_pct_themes``.
    """
    lexicon = cfg.fnmwcf_lexicon
    rows = []
    for tag in cfg.model_tags:
        g = resp[resp["model"] == tag]
        row = {"model": cfg.model_labels[tag]}
        flags = []
        for theme, terms in lexicon.items():
            hit = g[text_col].map(lambda t, tr=terms: theme_present(t, tr))
            row[f"cov_{theme}"] = round(100 * hit.mean(), 1)
            flags.append(hit)
        per_resp = pd.concat(flags, axis=1).mean(axis=1)
        row["mean_pct_themes"] = round(100 * per_resp.mean(), 1)
        rows.append(row)
    return pd.DataFrame(rows)

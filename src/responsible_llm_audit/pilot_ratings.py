"""Exploratory single-rater human rubric pilot summary.

Only DeepSeek-r1:8B carries variable ratings (n=13). The LLaMA/Mistral pilot entries are
uniform, non-informative entries (identical across the rated items, zero variance) and
are excluded from any comparison. No inter-rater reliability is computable with a single
rater.
"""
from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd

from .config import Config

AXES = ["accuracy", "cultural_relevance", "language_accessibility", "bias_avoidance"]


def pilot_summary(ratings: pd.DataFrame, cfg: Config) -> Dict[str, Any]:
    """Return descriptive summary of the DeepSeek pilot plus flags for other models."""
    rated = ratings[ratings["accuracy"].notna()].copy()
    ds = rated[rated["model"] == "deepseek-r1:8b"]
    summary: Dict[str, Any] = {
        "n_rated_rows_total": int(len(rated)),
        "n_by_model": rated["model"].value_counts().to_dict(),
        "reliability_computable": False,
        "deepseek_n": int(len(ds)),
        "deepseek_means": {a: round(ds[a].mean(), 3) for a in AXES},
        "deepseek_sem": {a: round(ds[a].std() / np.sqrt(len(ds)), 3) for a in AXES},
    }
    for tag in ("llama3.2:latest", "mistral:7b"):
        sub = rated[rated["model"] == tag]
        summary[f"{tag}_n"] = int(len(sub))
        summary[f"{tag}_uniform_noninformative_entries"] = (
            bool((sub[AXES].nunique() == 1).all()) if len(sub) else False
        )
    return summary


def pilot_table(ratings: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """DeepSeek pilot rubric table (mean and SEM per dimension) for the manuscript."""
    s = pilot_summary(ratings, cfg)
    rows = [
        {"statistic": "mean", **{a: s["deepseek_means"][a] for a in AXES}},
        {"statistic": "sem", **{a: s["deepseek_sem"][a] for a in AXES}},
    ]
    df = pd.DataFrame(rows)
    df.attrs["n"] = s["deepseek_n"]
    return df

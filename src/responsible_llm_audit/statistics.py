"""Descriptive statistics used in the manuscript.

No inferential hypothesis tests are performed, so no multiple-comparison correction is
applicable. Wilson intervals are conditional on the three fixed personas and their
repeated stochastic generations (they describe generation-level variability, not
population-level demographic inference).
"""
from __future__ import annotations

import math
from typing import Tuple

import pandas as pd

from .config import Config
from .markers import add_marker_flags


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score 95% confidence interval for a proportion, returned as percentages."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (round(100 * (centre - half), 1), round(100 * (centre + half), 1))


def cohen_h(p1: float, p2: float) -> float:
    """Cohen's h effect size for two proportions."""
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def marker_wilson_table(resp: pd.DataFrame, cfg: Config,
                        text_col: str = "full_cleaned") -> pd.DataFrame:
    """Per-model marker prevalence with Wilson 95% CIs (on ``text_col``)."""
    flagged = add_marker_flags(resp, cfg, text_col=text_col)
    rows = []
    for tag in cfg.model_tags:
        g = flagged[flagged["model"] == tag]
        n = len(g)
        row = {"model": cfg.model_labels[tag]}
        for marker in ("cultural", "crisis", "disclaimer"):
            k = int(g[f"marker_{marker}"].sum())
            row[f"{marker}_pct"] = round(100 * k / n, 1)
            lo, hi = wilson_ci(k, n)
            row[f"{marker}_ci_low"] = lo
            row[f"{marker}_ci_high"] = hi
        rows.append(row)
    return pd.DataFrame(rows)


def trimming_sensitivity(resp: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """Crisis-marker prevalence on full vs. 180-word display text, per model.

    Columns: ``model, crisis_full_pct, crisis_trimmed180_pct, delta_pts``.
    """
    full = add_marker_flags(resp, cfg, text_col="full_cleaned")
    disp = add_marker_flags(resp, cfg, text_col="display")
    rows = []
    for tag in cfg.model_tags:
        f = 100 * full.loc[full.model == tag, "marker_crisis"].mean()
        d = 100 * disp.loc[disp.model == tag, "marker_crisis"].mean()
        rows.append({
            "model": cfg.model_labels[tag],
            "crisis_full_pct": round(f, 1),
            "crisis_trimmed180_pct": round(d, 1),
            "delta_pts": round(f - d, 1),
        })
    return pd.DataFrame(rows)

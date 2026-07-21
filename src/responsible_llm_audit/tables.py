"""Generate all quantitative tables (written to ``outputs/tables``)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from .config import Config
from .fnmwcf import coverage_by_model
from .keywords import top_tokens_by_model
from .markers import add_marker_flags
from .personas import verify_personas
from .pilot_ratings import AXES, pilot_table
from .readability import readability_by_model
from .statistics import marker_wilson_table, trimming_sensitivity


def response_diagnostics(resp: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """Length / trimming / reasoning-trace diagnostics per model (display text)."""
    from .readability import flesch_reading_ease
    tmp = resp.copy()
    tmp["_fre"] = tmp["display"].map(flesch_reading_ease)
    rows = []
    for tag in cfg.model_tags:
        g = tmp[tmp.model == tag]
        rows.append({
            "model": cfg.model_labels[tag],
            "mean_words": round(g["display_words"].mean(), 1),
            "median_words": round(g["display_words"].median(), 1),
            "min_words": int(g["display_words"].min()),
            "max_words": int(g["display_words"].max()),
            "std_words": round(g["display_words"].std(), 1),
            "pct_at_180_cap": round(100 * g["trimmed_at_cap"].mean(), 1),
            "fre_mean": round(g["_fre"].mean(), 1),
            "pct_think_raw": round(100 * g["had_think_raw"].mean(), 1),
        })
    return pd.DataFrame(rows)


def generate_all_tables(resp: pd.DataFrame, ratings: pd.DataFrame,
                        cfg: Config, outdir: Path | None = None) -> Dict[str, Path]:
    """Compute and write every T_*.csv. Returns {name: path}."""
    outdir = outdir or cfg.output("tables")
    written: Dict[str, Path] = {}

    def _save(name: str, df: pd.DataFrame) -> None:
        p = outdir / name
        df.to_csv(p, index=False)
        written[name] = p

    # Markers (primary = full cleaned responses) with Wilson CIs
    _save("T_markers.csv", marker_wilson_table(resp, cfg, text_col="full_cleaned"))
    _save("T_trimming_sensitivity.csv", trimming_sensitivity(resp, cfg))
    _save("T_readability.csv", readability_by_model(resp, cfg, text_col="display"))
    _save("T_fnmwcf_coverage.csv", coverage_by_model(resp, cfg, text_col="display"))
    _save("T_top_keywords.csv", top_tokens_by_model(resp, cfg, text_col="display"))
    _save("T_response_diagnostics.csv", response_diagnostics(resp, cfg))
    _save("T_persona_verification.csv", verify_personas(cfg))

    pt = pilot_table(ratings, cfg)
    pt.insert(0, "n", pt.attrs.get("n"))
    _save("T_pilot_ratings.csv", pt)
    return written

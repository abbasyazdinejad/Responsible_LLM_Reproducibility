"""End-to-end orchestration used by the notebook, scripts, and tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd

from .config import Config, load_config
from .figures import generate_all_figures
from .io import load_pilot_ratings, load_prompts, load_responses
from .preprocessing import add_text_forms
from .prompts import prompt_accounting
from .tables import generate_all_tables
from .validation import ValidationResult, check_outputs_present, validate, write_report


@dataclass
class ReproductionArtifacts:
    resp: pd.DataFrame
    prompts: pd.DataFrame
    ratings: pd.DataFrame
    accounting: Dict[str, Any]
    tables: Dict[str, Any]
    figures: Dict[str, Any]
    validation: ValidationResult
    problems: list


def load_and_prepare(cfg: Config | None = None):
    """Load source data and attach the two analytical text forms."""
    cfg = cfg or load_config()
    resp = add_text_forms(load_responses(cfg), cfg)
    prompts = load_prompts(cfg)
    ratings = load_pilot_ratings(cfg)
    return cfg, resp, prompts, ratings


def run_full_reproduction(cfg: Config | None = None,
                          make_figures: bool = True) -> ReproductionArtifacts:
    """Run the full pipeline: load -> tables -> figures -> validate."""
    cfg, resp, prompts, ratings = load_and_prepare(cfg)
    accounting = prompt_accounting(prompts, resp, cfg)
    tables = generate_all_tables(resp, ratings, cfg)
    figures = generate_all_figures(resp, ratings, cfg) if make_figures else {}
    res = validate(resp, prompts, ratings, cfg)
    problems = check_outputs_present(cfg, list(tables.keys()))
    write_report(res, problems, cfg)
    return ReproductionArtifacts(resp, prompts, ratings, accounting,
                                 tables, figures, res, problems)

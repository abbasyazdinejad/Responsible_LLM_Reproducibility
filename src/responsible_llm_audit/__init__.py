"""responsible_llm_audit -- reproducible equity-first LLM audit pipeline.

Public API re-exports the core building blocks so the notebook, scripts, and tests all
import the *same* implementation (no duplicated analysis logic).
"""
from __future__ import annotations

from .config import Config, load_config, find_repo_root
from .io import (
    load_responses, load_prompts, load_pilot_ratings, load_persona_metadata,
    MissingFileError, SchemaError, EmptyDataError,
)
from .preprocessing import add_text_forms, strip_reasoning_traces, trim_to_words
from .markers import marker_rates, add_marker_flags
from .readability import readability_by_model, flesch_kincaid_grade
from .fnmwcf import coverage_by_model
from .keywords import top_tokens_by_model, top_tokens
from .prompts import prompt_accounting
from .personas import verify_personas
from .pilot_ratings import pilot_summary, pilot_table
from .statistics import wilson_ci, cohen_h, marker_wilson_table, trimming_sensitivity
from .tables import generate_all_tables, response_diagnostics
from .figures import generate_all_figures, EXPECTED_FIGURES
from .validation import validate, check_outputs_present, write_report, ValidationResult
from .reproduce import run_full_reproduction, load_and_prepare, ReproductionArtifacts

__version__ = "1.0.0"

__all__ = [
    "Config", "load_config", "find_repo_root",
    "load_responses", "load_prompts", "load_pilot_ratings", "load_persona_metadata",
    "MissingFileError", "SchemaError", "EmptyDataError",
    "add_text_forms", "strip_reasoning_traces", "trim_to_words",
    "marker_rates", "add_marker_flags", "readability_by_model", "flesch_kincaid_grade",
    "coverage_by_model", "top_tokens_by_model", "top_tokens", "prompt_accounting",
    "verify_personas", "pilot_summary", "pilot_table",
    "wilson_ci", "cohen_h", "marker_wilson_table", "trimming_sensitivity",
    "generate_all_tables", "response_diagnostics", "generate_all_figures", "EXPECTED_FIGURES",
    "validate", "check_outputs_present", "write_report", "ValidationResult",
    "run_full_reproduction", "load_and_prepare", "ReproductionArtifacts",
    "__version__",
]

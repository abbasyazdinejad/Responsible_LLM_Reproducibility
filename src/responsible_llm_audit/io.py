"""Input/output: loading and validating the study-generated source files."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import Config


class MissingFileError(FileNotFoundError):
    """A required input file is absent."""


class SchemaError(ValueError):
    """A loaded file is missing required columns."""


class EmptyDataError(ValueError):
    """A loaded file contains no rows."""


def _require(path: Path) -> Path:
    if not path.exists():
        raise MissingFileError(
            f"Required input not found: {path}\n"
            f"See data/README.md for how to obtain / place study data."
        )
    return path


def _check_columns(df: pd.DataFrame, needed: Iterable[str], src: str) -> None:
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise SchemaError(f"{src} is missing required columns: {missing}")
    if len(df) == 0:
        raise EmptyDataError(f"{src} contains no rows.")


def load_responses(cfg: Config) -> pd.DataFrame:
    """Load and concatenate the raw model-response files (one per model).

    Returns a long DataFrame with columns ``[id, model, timestamp, context, prompt,
    response]`` and exactly ``responses_per_model`` rows for each configured model.
    """
    frames = []
    file_map = cfg.settings["data"]["response_files"]
    for tag in cfg.model_tags:
        fname = file_map[tag]
        path = _require(cfg.responses_dir / fname)
        df = pd.read_csv(path, engine="python")
        df["model"] = tag
        _check_columns(df, ["id", "context", "prompt", "response"], fname)
        frames.append(df)
    resp = pd.concat(frames, ignore_index=True)

    expected = int(cfg.settings["data"]["responses_per_model"])
    for tag in cfg.model_tags:
        n = int((resp["model"] == tag).sum())
        if n != expected:
            raise SchemaError(
                f"Expected {expected} responses for {tag}, found {n}."
            )
    return resp


def load_prompts(cfg: Config) -> pd.DataFrame:
    path = _require(cfg.prompts_dir / cfg.settings["data"]["prompts_file"])
    df = pd.read_csv(path, engine="python")
    _check_columns(df, ["id", "context", "prompt"], path.name)
    return df


def load_pilot_ratings(cfg: Config) -> pd.DataFrame:
    """Load the exploratory single-rater rubric pilot ratings (rated rows only)."""
    path = _require(cfg.ratings_dir / cfg.settings["data"]["ratings_file"])
    df = pd.read_csv(path, engine="python")
    _check_columns(
        df,
        ["id", "model", "accuracy", "cultural_relevance",
         "language_accessibility", "bias_avoidance"],
        path.name,
    )
    return df


def load_persona_metadata(cfg: Config) -> pd.DataFrame:
    path = _require(cfg.prompts_dir / cfg.settings["data"]["persona_file"])
    return pd.read_csv(path, engine="python")

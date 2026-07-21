"""Configuration loading and repository-path resolution.

All analysis settings live in ``config/*.yaml`` / ``config/*.json`` rather than being
scattered through the code. This module locates the repository root robustly (so the
package works whether it is run from the notebook, a script, or an editable install)
and exposes a single :class:`Config` object.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError("PyYAML is required. Install with `pip install pyyaml`.") from exc


class ConfigError(RuntimeError):
    """Raised when configuration is missing or malformed."""


def find_repo_root(start: Path | None = None) -> Path:
    """Return the repository root.

    Resolution order: ``REPRO_REPO_ROOT`` environment variable, then the first parent
    directory (walking up from this file) that contains ``pyproject.toml``.
    """
    env = os.environ.get("REPRO_REPO_ROOT")
    if env:
        root = Path(env).expanduser().resolve()
        if not root.exists():
            raise ConfigError(f"REPRO_REPO_ROOT points to a missing path: {root}")
        return root
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback: src/responsible_llm_audit/config.py -> repo root is parents[2]
    return here.parents[2]


@dataclass(frozen=True)
class Config:
    """Immutable, fully-resolved analysis configuration."""

    root: Path
    settings: Dict[str, Any]
    marker_patterns: Dict[str, str]
    fnmwcf_lexicon: Dict[str, List[str]]
    expected_results: Dict[str, Any]

    # --- convenience accessors ---------------------------------------------
    @property
    def model_tags(self) -> List[str]:
        return list(self.settings["models"]["tags"])

    @property
    def model_labels(self) -> Dict[str, str]:
        return dict(self.settings["models"]["labels"])

    @property
    def ordered_labels(self) -> List[str]:
        return [self.model_labels[t] for t in self.model_tags]

    @property
    def display_word_cap(self) -> int:
        return int(self.settings["preprocessing"]["display_word_cap"])

    @property
    def stopwords(self) -> set[str]:
        return set(self.settings["keywords"]["stopwords"])

    @property
    def min_token_length(self) -> int:
        return int(self.settings["keywords"]["min_token_length"])

    @property
    def top_n_tokens(self) -> int:
        return int(self.settings["keywords"]["top_n"])

    # --- path helpers ------------------------------------------------------
    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    @property
    def data_dir(self) -> Path:
        return self.path("data")

    @property
    def responses_dir(self) -> Path:
        return self.path("data", "responses")

    @property
    def prompts_dir(self) -> Path:
        return self.path("data", "prompts")

    @property
    def ratings_dir(self) -> Path:
        return self.path("data", "ratings")

    @property
    def raw_dir(self) -> Path:
        return self.path("data", "raw")

    @property
    def outputs_dir(self) -> Path:
        return self.path("outputs")

    def output(self, kind: str) -> Path:
        d = self.path("outputs", kind)
        d.mkdir(parents=True, exist_ok=True)
        return d


def _load_json(p: Path) -> Any:
    if not p.exists():
        raise ConfigError(f"Missing config file: {p}")
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_config(root: Path | None = None) -> Config:
    """Load and validate the full configuration."""
    root = root or find_repo_root()
    cfg_dir = root / "config"
    settings_path = cfg_dir / "analysis_config.yaml"
    if not settings_path.exists():
        raise ConfigError(f"Missing {settings_path}")
    with settings_path.open(encoding="utf-8") as fh:
        settings = yaml.safe_load(fh)

    marker_patterns = _load_json(cfg_dir / "marker_patterns.json")
    fnmwcf_lexicon = _load_json(cfg_dir / "fnmwcf_lexicon.json")
    expected_results = _load_json(cfg_dir / "expected_results.json")

    # minimal schema validation
    for key in ("models", "decoding", "preprocessing", "keywords"):
        if key not in settings:
            raise ConfigError(f"analysis_config.yaml missing top-level key: {key}")
    for key in ("crisis", "disclaimer", "cultural"):
        if key not in marker_patterns:
            raise ConfigError(f"marker_patterns.json missing key: {key}")

    return Config(
        root=root,
        settings=settings,
        marker_patterns=marker_patterns,
        fnmwcf_lexicon=fnmwcf_lexicon,
        expected_results=expected_results,
    )

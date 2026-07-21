"""Shared pytest fixtures.

Loads the data once and runs the full reproduction (tables + figures) a single time,
so value tests and output-existence tests share the same artifacts.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import pytest

# Make the package importable without an editable install.
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
warnings.filterwarnings("ignore")

import responsible_llm_audit as rla  # noqa: E402


@pytest.fixture(scope="session")
def cfg():
    return rla.load_config()


@pytest.fixture(scope="session")
def prepared(cfg):
    _cfg, resp, prompts, ratings = rla.load_and_prepare(cfg)
    return {"cfg": _cfg, "resp": resp, "prompts": prompts, "ratings": ratings}


@pytest.fixture(scope="session")
def artifacts(cfg):
    """Run the full pipeline once (writes outputs/ tables + figures)."""
    return rla.run_full_reproduction(cfg, make_figures=True)

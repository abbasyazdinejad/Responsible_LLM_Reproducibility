"""Make the package importable whether or not it has been pip-installed.

Adds ``<repo>/src`` to ``sys.path`` if ``responsible_llm_audit`` is not already
importable. Every script imports this first.
"""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_importable() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    try:
        import responsible_llm_audit  # noqa: F401
    except ImportError:
        sys.path.insert(0, str(repo_root / "src"))
    return repo_root

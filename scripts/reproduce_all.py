#!/usr/bin/env python3
"""Reproduce all derived tables, empirical figures, and the validation report.

Usage:
    python scripts/reproduce_all.py

Exits with a non-zero status if inputs are invalid, expected values do not match,
or any expected output is missing/empty.
"""
from __future__ import annotations

import sys
import warnings

from _bootstrap import ensure_importable

ensure_importable()
warnings.filterwarnings("ignore")  # keep the console clean; correctness is checked below

import responsible_llm_audit as rla  # noqa: E402


def main() -> int:
    cfg = rla.load_config()
    print(f"[1/4] Loading and preparing data (repo: {cfg.root})...")
    art = rla.run_full_reproduction(cfg, make_figures=True)

    print(f"[2/4] Tables written: {len(art.tables)} -> outputs/tables/")
    for name in sorted(art.tables):
        print(f"        {name}")
    print(f"[3/4] Figures written: {len(art.figures)} -> outputs/figures/")
    for name in sorted(art.figures):
        print(f"        {name}")

    print("[4/4] Validation:")
    for c in art.validation.checks:
        flag = "ok " if c.ok else "XX "
        print(f"        [{flag}] {c.name}: observed={c.observed} expected={c.expected}")

    ok = art.validation.passed and not art.problems
    print("-" * 60)
    print(f"Corpus: {art.accounting['n_responses_total']} responses, "
          f"{art.accounting['n_unique_personas']} personas, "
          f"{art.accounting['n_responses_total'] // 3} per model.")
    print(f"Value checks passed : {art.validation.passed}")
    print(f"Output problems     : {art.problems if art.problems else 'none'}")
    print(f"Validation report   : outputs/validation/validation_report.json")
    print("RESULT:", "SUCCESS" if ok else "FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

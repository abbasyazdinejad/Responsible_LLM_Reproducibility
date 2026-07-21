#!/usr/bin/env python3
"""Regenerate only the quantitative tables (outputs/tables/)."""
from __future__ import annotations
import sys, warnings
from _bootstrap import ensure_importable
ensure_importable(); warnings.filterwarnings("ignore")
import responsible_llm_audit as rla

def main() -> int:
    cfg, resp, prompts, ratings = rla.load_and_prepare()
    written = rla.generate_all_tables(resp, ratings, cfg)
    for name in sorted(written):
        print("wrote", name)
    print(f"[OK] {len(written)} tables -> outputs/tables/")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Regenerate only the empirical figures (outputs/figures/)."""
from __future__ import annotations
import sys, warnings
from _bootstrap import ensure_importable
ensure_importable(); warnings.filterwarnings("ignore")
import responsible_llm_audit as rla

def main() -> int:
    cfg, resp, prompts, ratings = rla.load_and_prepare()
    written = rla.generate_all_figures(resp, ratings, cfg)
    for name in sorted(written):
        print("wrote", name)
    print(f"[OK] {len(written)} figures -> outputs/figures/")
    return 0

if __name__ == "__main__":
    sys.exit(main())

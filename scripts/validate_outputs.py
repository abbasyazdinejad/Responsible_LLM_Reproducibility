#!/usr/bin/env python3
"""Validate computed values against the expected manuscript results and check outputs."""
from __future__ import annotations
import sys, warnings
from _bootstrap import ensure_importable
ensure_importable(); warnings.filterwarnings("ignore")
import responsible_llm_audit as rla

def main() -> int:
    cfg, resp, prompts, ratings = rla.load_and_prepare()
    res = rla.validate(resp, prompts, ratings, cfg)
    tables = [f"T_{n}.csv" for n in ["markers","readability","fnmwcf_coverage","trimming_sensitivity","top_keywords","response_diagnostics","pilot_ratings","persona_verification"]]
    problems = rla.check_outputs_present(cfg, tables)
    rla.write_report(res, problems, cfg)
    for c in res.checks:
        print(("ok " if c.ok else "XX "), c.name, "obs=", c.observed, "exp=", c.expected)
    print("value_checks_passed:", res.passed, "| output_problems:", problems if problems else "none")
    return 0 if (res.passed and not problems) else 1

if __name__ == "__main__":
    sys.exit(main())

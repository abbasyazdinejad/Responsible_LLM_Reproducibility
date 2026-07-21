#!/usr/bin/env python3
"""Build notebooks/ScientificReports_Full_Reproduction.ipynb (imports the package)."""
from __future__ import annotations
from pathlib import Path
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

REPO = Path(__file__).resolve().parents[1]
cells = []
def md(t): cells.append(new_markdown_cell(t))
def code(t): cells.append(new_code_cell(t))

md("""# Scientific Reports — Full Reproduction

**Paper:** *Responsible Use of Large Language Models in Digital Health: An Equity-First Governance Framework*

This notebook reproduces **all data-derived empirical figures and quantitative tables** reported in the
manuscript, using the reusable functions in the `responsible_llm_audit` package (so the notebook, the
command-line scripts, and the tests all share one implementation). It runs top-to-bottom from a fresh
kernel, uses **no absolute paths and no external subprocess**, and fails clearly if a required input or
expected output is missing.

> Figures 8–10 in the manuscript are conceptual / methodological diagrams created in the manuscript itself
> and are **not** generated here; this notebook regenerates the seven data-derived empirical figures.""")

md("## 1. Setup (make the package importable; locate the repository root)")
code("""import sys, warnings
from pathlib import Path

def find_repo_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    raise FileNotFoundError("Could not locate repository root (pyproject.toml).")

REPO = find_repo_root(Path.cwd())
sys.path.insert(0, str(REPO / "src"))
warnings.filterwarnings("ignore")

import responsible_llm_audit as rla
cfg = rla.load_config(REPO)
print("Package version:", rla.__version__)
print("Repository root folder:", REPO.name)  # name only (portable; no absolute path in output)""")


md("## 2. Load and validate the source data")
code("""cfg, resp, prompts, ratings = rla.load_and_prepare(cfg)
print("Loaded", len(resp), "responses;", len(prompts), "prompt rows;",
      int(ratings['accuracy'].notna().sum()), "pilot ratings")
resp[["id", "model", "context"]].head(3)""")

md("## 3. Prompt and response accounting")
code("""acct = rla.prompt_accounting(prompts, resp, cfg)
for k, v in acct.items():
    print(f"{k}: {v}")""")

md("""## 4. Preprocessing — two analytical text forms
`full_cleaned` = reasoning traces removed (used for content markers and the trimming sensitivity);
`display` = full cleaned text trimmed to the 180-word display cap (used for readability, length, keywords).""")
code("""resp[["model", "full_words", "display_words", "trimmed_at_cap"]].groupby("model").mean(numeric_only=True).round(1)""")

md("## 5. Safety and cultural markers (full cleaned responses) with Wilson 95% CIs")
code("""markers_ci = rla.marker_wilson_table(resp, cfg, text_col="full_cleaned")
markers_ci""")

md("## 6. Trimming sensitivity (full vs. 180-word display text)")
code("""sens = rla.trimming_sensitivity(resp, cfg)
print("The 180-word display trim materially reduces the DeepSeek crisis marker;\\n"
      "content markers are therefore reported on full responses.")
sens""")

md("## 7. Readability (display responses)")
code("""readability = rla.readability_by_model(resp, cfg, text_col="display")
readability""")

md("## 8. FNMWCF lexical coverage (proxy only; not cultural adequacy)")
code("""coverage = rla.coverage_by_model(resp, cfg, text_col="display")
coverage""")

md("## 9. Keyword framing (same stopword pipeline used for Table 5 and Figure 6)")
code("""keywords = rla.top_tokens_by_model(resp, cfg, text_col="display", n=10)
keywords.pivot(index="rank", columns="model", values="token")""")

md("## 10. Response diagnostics (length, trimming rate, reasoning traces)")
code("""rla.response_diagnostics(resp, cfg)""")

md("## 11. Exploratory single-rater human rubric pilot")
code("""pilot = rla.pilot_summary(ratings, cfg)
print("DeepSeek pilot n =", pilot["deepseek_n"], "| reliability computable:", pilot["reliability_computable"])
print("means:", pilot["deepseek_means"])
print("Non-DeepSeek entries are uniform / non-informative and excluded from any comparison.")
rla.pilot_table(ratings, cfg)""")

md("## 12. Persona verification against the CCHS PUMF")
code("""# Uses data/raw/pumf_cchs.csv if present; otherwise reports documented CCHS-consistent counts.
rla.verify_personas(cfg)""")

md("## 13. Generate all quantitative tables -> outputs/tables/")
code("""tables = rla.generate_all_tables(resp, ratings, cfg)
for name in sorted(tables):
    print("wrote", name)""")

md("## 14. Generate all empirical figures inline -> outputs/figures/")
code("""from IPython.display import Image, display
figures = rla.generate_all_figures(resp, ratings, cfg)
for name in rla.EXPECTED_FIGURES:
    display(Image(filename=str(figures[name])))""")

md("## 15. Validate computed values against the expected manuscript results")
code("""res = rla.validate(resp, prompts, ratings, cfg)
problems = rla.check_outputs_present(cfg, list(tables.keys()))
rla.write_report(res, problems, cfg)
for c in res.checks:
    print(("ok " if c.ok else "XX "), c.name, "obs=", c.observed, "exp=", c.expected)
print("value checks passed:", res.passed, "| output problems:", problems or "none")""")

md("## 16. Final assertions (fail if any expected output is missing/empty)")
code("""missing = [f for f in rla.EXPECTED_FIGURES
           if not (cfg.path('outputs','figures',f).exists() and cfg.path('outputs','figures',f).stat().st_size > 5000)]
assert not missing, f"missing/empty figures: {missing}"
assert res.passed, "expected-value validation failed"
assert not problems, problems
print("ALL CHECKS PASSED — figures and tables regenerated and validated.")""")

nb = new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
out = REPO / "notebooks" / "ScientificReports_Full_Reproduction.ipynb"
nbf.write(nb, out)
print("wrote", out, "with", len(cells), "cells")

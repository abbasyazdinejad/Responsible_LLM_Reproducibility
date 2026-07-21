# Responsible LLM Reproducibility — Equity-First Audit of Open-Source LLMs for Digital-Health Guidance


This repository reproduces **all data-derived empirical figures and quantitative tables** in the paper
from the stored model responses, using a small, documented Python package. It runs fully offline and is
validated against the manuscript's key values.

---

## Study in brief

Three open-source LLMs (**DeepSeek-r1:8B**, **LLaMA-3.2:latest**, **Mistral-7B**) were queried with three
FNMWCF-informed, CCHS-consistent persona prompts, 150 stochastic generations each (temperature 0.7),
giving **450 responses per model** and **1,350 in total**. We analyse the corpus with automated,
reproducible text metrics — explicit safety/cultural markers, readability, FNMWCF lexical coverage, keyword
framing, and a trimming sensitivity analysis — and a small exploratory single-rater rubric pilot.

### Final analytical design
- Responses are cleaned into two forms: a **full cleaned** response (`<think>` traces removed) and a
  **180-word display** response.
- **Safety/cultural markers** are computed on the **full cleaned** responses.
- **Readability, length, and keyword framing** are computed on the **display** responses.
- A **trimming sensitivity** analysis compares marker prevalence between the two forms.

### Important limitations
Three predefined (non-representative) personas with confounded demographics; a single-rater pilot with no
computable reliability; lexical (keyword) proxies that do not establish cultural adequacy; readability is
not comprehension; English only; mutable model tags (digests not recorded). See
[`docs/Limitations.md`](docs/Limitations.md).

---

## Repository structure

See [`docs/Repository_Contents.md`](docs/Repository_Contents.md). Key locations: `src/responsible_llm_audit`
(the analysis package used by the notebook, scripts, and tests), `notebooks/` (end-to-end notebook),
`scripts/` (CLI), `config/` (all settings), `data/` (study data + CCHS instructions), `outputs/`
(regenerated figures/tables), `tests/` (pytest), `docs/` (documentation).

## Software requirements
Python ≥ 3.9 with `pandas`, `numpy`, `matplotlib`, `scipy`, `PyYAML` (plus `jupyterlab`/`pytest` for the
notebook and tests). No external NLP corpus is required.

## Environment setup

```bash
# Option A: conda
conda env create -f environment.yml
conda activate responsible-llm-audit

# Option B: pip
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## CCHS source data (optional; not redistributed)
The three personas are defined by CCHS 2019–2020 PUMF variables. The raw PUMF is **not** included and is
only needed to *re-verify* the personas. To add it, download from Statistics Canada and place
`pumf_cchs.csv` in `data/raw/` — full instructions and licensing are in
[`data/README.md`](data/README.md):
- Info: <https://www150.statcan.gc.ca/n1/pub/82m0013x/82m0013x2024001-eng.htm>
- CSV (ZIP): <https://www150.statcan.gc.ca/n1/pub/82m0013x/2024001/2019-2020_CSV.zip>

## Reproduce

```bash
python scripts/verify_environment.py     # check env + inputs
python scripts/reproduce_all.py          # regenerate all tables + figures + validation report
pytest                                    # run the test suite
```

Or the notebook:
```bash
jupyter lab notebooks/ScientificReports_Full_Reproduction.ipynb
```

**Expected runtime:** ~30–90 seconds on a laptop (no GPU, no network).

## Expected outputs
- `outputs/tables/`: `T_markers.csv`, `T_trimming_sensitivity.csv`, `T_readability.csv`,
  `T_fnmwcf_coverage.csv`, `T_top_keywords.csv`, `T_response_diagnostics.csv`, `T_pilot_ratings.csv`,
  `T_persona_verification.csv`.
- `outputs/figures/`: `fig_markers.png`, `fig_readability.png`, `fig_fnmwcf.png`, `fig_length.png`,
  `fig_variability.png`, `fig_keywords.png`, `fig_pilot.png` (the 7 empirical figures; manuscript
  Figures 8–10 are conceptual diagrams and are not generated here).
- `outputs/validation/validation_report.json`.

## Expected key results
| Metric | DeepSeek-r1:8B | LLaMA-3.2:latest | Mistral-7B |
|---|---|---|---|
| Crisis guidance (full responses) | **71.3%** | **99.6%** | **99.6%** |
| Crisis guidance (180-word display; sensitivity) | 30.0% | 97.6% | 96.9% |
| Disclaimer / referral | 0.2% | 0.0% | 0.0% |
| Cultural marker (lexical) | 100% | 100% | 100% |
| Readability (FKGL) | ≈10.8 | ≈9.8 | ≈10.4 |

Responses per model = 450; total = 1,350; exploratory pilot usable n = 13 (DeepSeek).

## Tests
`pytest` verifies the sample accounting, marker values (full and trimmed), disclaimer/cultural rates, FKGL
means, pilot n, model-name consistency, and that every expected figure and table exists, is non-empty, and
contains no NaNs.

## Citation
See [`CITATION.cff`](CITATION.cff). Please cite both the paper and this software. A DOI will be added when
assigned (none is claimed here).

## Data and code availability
Code: MIT ([`LICENSE`](LICENSE)). Study-generated data (prompts, model responses, pilot ratings) are
included and redistributable. The CCHS PUMF is third-party (Statistics Canada Open Licence) and must be
obtained separately.

## Contact
Abbas Yazdinejad — `Abbas.Yazdinejad@uregina.ca`; Jude Kong — `jude.kong@utoronto.ca`.

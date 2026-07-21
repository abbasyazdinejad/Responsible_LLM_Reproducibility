# Data

This directory holds the study-generated data required to reproduce the analysis, plus a placeholder for
the third-party Statistics Canada source data (which is **not** redistributed here).

```
data/
├── prompts/     prompts_cchs.csv, persona_metadata.csv   (study-generated)
├── responses/   ollama_results_<model>.csv               (study-generated model outputs)
├── ratings/     pilot_ratings.csv                         (study-generated pilot ratings)
├── derived/     (reserved for user-generated intermediates)
└── raw/         .gitkeep only — place the CCHS PUMF here (see below)
```

## 1. Study-generated data (included, redistributable)

| File | What it is | Rows | Key columns |
|---|---|---|---|
| `prompts/prompts_cchs.csv` | The 3 FNMWCF-informed persona prompts, each repeated 150× | 450 | `id, context, prompt` |
| `prompts/persona_metadata.csv` | The 3 predefined persona profiles (CCHS variable values) | 3 | `province, sex, age_group, depression_severity, life_satisfaction` |
| `responses/ollama_results_deepseek-r1_8b.csv` | Raw DeepSeek-r1:8B responses | 450 | `id, model, timestamp, context, prompt, response` |
| `responses/ollama_results_llama3.2_latest.csv` | Raw LLaMA-3.2:latest responses | 450 | same |
| `responses/ollama_results_mistral_7b.csv` | Raw Mistral-7B responses | 450 | same |
| `ratings/pilot_ratings.csv` | Exploratory single-rater rubric pilot (rated rows only) | 19 | `id, model, accuracy, cultural_relevance, language_accessibility, bias_avoidance` |

These are outputs of the study (model generations and the pilot ratings), not Statistics Canada data. See
`../docs/Data_Dictionary.md` for full details.

## 2. Statistics Canada CCHS 2019–2020 PUMF (NOT included — download separately)

The personas are defined by variables from the **Canadian Community Health Survey (CCHS) 2019–2020 Public
Use Microdata File (PUMF)**. The raw PUMF is **not redistributed** in this repository. It is only needed if
you wish to *re-verify* that the three personas correspond to real CCHS respondent records; the rest of the
pipeline runs without it (persona verification falls back to documented match counts).

To obtain it:

1. **Information page:**
   <https://www150.statcan.gc.ca/n1/pub/82m0013x/82m0013x2024001-eng.htm>
2. **Direct 2019–2020 CSV download:**
   <https://www150.statcan.gc.ca/n1/pub/82m0013x/2024001/2019-2020_CSV.zip>
3. Download the ZIP file and **extract** it.
4. Locate the microdata CSV inside the extracted `2019-2020_CSV/Data_Donnees/` folder
   (filename `pumf_cchs.csv`).
5. Copy it to:
   ```
   data/raw/pumf_cchs.csv
   ```
6. The preprocessing code (`responsible_llm_audit.personas`) locates it at that path, reads only the columns
   listed in `config/analysis_config.yaml` (`GEOGPRV, DHH_SEX, DHHGAGE, DEPDVSEV, SWL_005`), and validates
   the three persona profiles against it. If the file is absent, `verify_personas` reports the documented
   match counts (361 / 1,551 / 2,612) with `source = "documented"`.

**Expected filename:** `pumf_cchs.csv` (override via `data.pumf_filename` in `config/analysis_config.yaml`).

### Data licence
The CCHS PUMF is distributed by Statistics Canada under the **Statistics Canada Open Licence**
(<https://www.statcan.gc.ca/en/reference/licence>). Users must obtain it directly from Statistics Canada
and comply with that licence. The MIT licence in this repository applies to the **code only**, not to any
third-party data.

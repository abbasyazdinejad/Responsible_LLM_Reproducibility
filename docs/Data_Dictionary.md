# Data Dictionary

All row/column counts are as shipped. "Type" is raw (as generated), derived (computed from raw), or
analytical (a reported result). Generating script/function names refer to the `responsible_llm_audit`
package.

## Input data (`data/`)

### `data/prompts/prompts_cchs.csv` — raw, redistributable
- **Purpose:** the instantiated prompts sent to each model.
- **Rows × cols:** 450 × 3. **Columns:** `id` (1–450), `context` (persona string), `prompt` (full text).
- **Note:** 3 unique persona contexts / prompt texts, each appearing 150 times.
- **Generating step:** study prompt construction (FNMWCF-informed template + persona).
- **Manuscript link:** Table 1 (corpus), Methods "Prompt construction".

### `data/prompts/persona_metadata.csv` — raw, redistributable
- **Purpose:** the three predefined persona profiles.
- **Rows × cols:** 3 × 5. **Columns:** `province, sex, age_group, depression_severity, life_satisfaction`.
- **Manuscript link:** Methods "Data and persona construction"; `T_persona_verification.csv`.

### `data/responses/ollama_results_<model>.csv` — raw, redistributable (study outputs)
- **Purpose:** raw model generations (150 per persona × 3 personas = 450 per model).
- **Rows × cols:** 450 × 6 each. **Columns:** `id, model, timestamp, context, prompt, response`.
- **Key variable:** `response` (raw text; DeepSeek responses may contain `<think>` traces).
- **Loaded by:** `io.load_responses`.
- **Manuscript link:** all automated metrics (Tables 2–5, Figures 1–6).

### `data/ratings/pilot_ratings.csv` — raw, redistributable (study outputs)
- **Purpose:** exploratory single-rater rubric pilot (rated rows only).
- **Rows × cols:** 19 × 6. **Columns:** `id, model, accuracy, cultural_relevance,
  language_accessibility, bias_avoidance` (0–3 ordinal).
- **Note:** DeepSeek has 13 variable ratings; LLaMA/Mistral entries (3 each) are uniform, non-informative.
- **Loaded by:** `io.load_pilot_ratings`. **Manuscript link:** Table 6, Figure 7.

### `data/raw/pumf_cchs.csv` — third-party, NOT included
- **Purpose:** CCHS 2019–2020 PUMF; used only to verify persona profiles.
- **Source/licence:** Statistics Canada Open Licence — download separately (see `data/README.md`).

## Derived / analytical outputs (`outputs/tables/`)

| File | Type | Generating function | Rows | Manuscript |
|---|---|---|---|---|
| `T_markers.csv` | analytical | `statistics.marker_wilson_table` (full responses) | 3 | Table 2, Fig 1 |
| `T_trimming_sensitivity.csv` | analytical | `statistics.trimming_sensitivity` | 3 | Results/Methods (sensitivity) |
| `T_readability.csv` | analytical | `readability.readability_by_model` (display) | 3 | Table 3, Fig 2 |
| `T_fnmwcf_coverage.csv` | analytical | `fnmwcf.coverage_by_model` (display) | 3 | Fig 3 |
| `T_top_keywords.csv` | analytical | `keywords.top_tokens_by_model` (display) | 30 | Table 5, Fig 6 |
| `T_response_diagnostics.csv` | analytical | `tables.response_diagnostics` | 3 | Table 4, Fig 4 |
| `T_pilot_ratings.csv` | analytical | `pilot_ratings.pilot_table` | 2 | Table 6, Fig 7 |
| `T_persona_verification.csv` | analytical | `personas.verify_personas` | 3 | Methods (persona) |

### Machine-readable columns
- `T_markers.csv`: `model, cultural_pct, cultural_ci_low, cultural_ci_high, crisis_pct, crisis_ci_low,
  crisis_ci_high, disclaimer_pct, disclaimer_ci_low, disclaimer_ci_high`.
- `T_trimming_sensitivity.csv`: `model, crisis_full_pct, crisis_trimmed180_pct, delta_pts`.
- `T_readability.csv`: `model, avg_sentence_len_words, avg_chars_per_word, fkgl_mean, fkgl_sd`.
- `T_fnmwcf_coverage.csv`: `model, cov_<theme>×4, mean_pct_themes`.
- `T_top_keywords.csv`: `model, rank, token, count`.
- `T_response_diagnostics.csv`: `model, mean_words, median_words, min_words, max_words, std_words,
  pct_at_180_cap, fre_mean, pct_think_raw`.
- `T_pilot_ratings.csv`: `n, statistic, accuracy, cultural_relevance, language_accessibility, bias_avoidance`.
- `T_persona_verification.csv`: `province, sex, age_group, depression_severity, life_satisfaction,
  matching_cchs_records, source`.

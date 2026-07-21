# Data Provenance

Complete analytical path from the survey source to the reported values.

```
Statistics Canada CCHS 2019–2020 PUMF
        │  (used only to verify persona profiles; not redistributed here)
        ▼
verification of three PREDEFINED, CCHS-consistent persona profiles
        │  (SK/Female/25–34; SK/Male/50–64; BC/Female/50–64)
        ▼
FNMWCF-informed prompt construction  (3 persona prompts)
        ▼
150 stochastic generations per persona per model  (temperature 0.7)
        ▼
raw model responses  (450 per model; 1,350 total)  -> data/responses/
        ▼
removal of non-user-facing reasoning traces (<think> ... </think>)
        ▼
two analytical text forms:
    A. full cleaned responses   (no word trim)
    B. 180-word display responses
        │
        ├── A  →  safety markers, cultural markers, trimming sensitivity
        │
        └── B  →  readability, response length, keyword framing
        ▼
separate exploratory single-rater rubric pilot  (data/ratings/)
        ▼
tables, figures, diagnostics, validation, and the manuscript values
```

## Statements of scope and limitation (important)

- The three personas were **predefined**. They were **not sampled** from the CCHS and are **not**
  statistically representative of any population. Weights were not applied.
- They were **verified as CCHS-consistent**: each profile corresponds to real respondent records in the
  CCHS 2019–2020 PUMF (documented match counts: 361, 1,551, and 2,612). Verification is performed by
  `responsible_llm_audit.personas.verify_personas` when the PUMF is present.
- The CCHS PUMF contains **no direct Indigenous-identity variable**. The personas therefore cannot be
  Indigenous-specific.
- The prompts are **FNMWCF-informed**, not community-validated. Use of a published cultural framework does
  not establish community endorsement or cultural safety.
- **Why two text forms?** Content markers (crisis/disclaimer/cultural) concern whether the model *provided*
  the guidance at all, so they are computed on the **full cleaned** responses. Readability, length, and
  keyword framing describe the user-facing **display** text, so they use the 180-word display form. A
  sensitivity analysis compares marker prevalence between the two forms and shows the 180-word trim
  materially reduces the DeepSeek crisis marker (71.3% → 30.0%), motivating the full-response choice.

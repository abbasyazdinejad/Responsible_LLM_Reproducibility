# Repository Contents

```
Responsible_LLM_Reproducibility_GitHub/
├── README.md, LICENSE, CITATION.cff, .gitignore
├── requirements.txt, environment.yml, pyproject.toml, MANIFEST.in
├── data/            study-generated data (+ instructions to obtain the CCHS PUMF)
├── notebooks/       ScientificReports_Full_Reproduction.ipynb (end-to-end, imports the package)
├── src/responsible_llm_audit/   modular, documented analysis package (single source of logic)
├── scripts/         reproduce_all.py, generate_tables.py, generate_figures.py,
│                    validate_outputs.py, verify_environment.py
├── config/          analysis_config.yaml, marker_patterns.json, fnmwcf_lexicon.json, expected_results.json
├── outputs/         figures/, tables/, diagnostics/, validation/ (regenerated, committed)
├── docs/            Data_Dictionary, Data_Provenance, Methods_Reproduction, Code_to_Paper_Map,
│                    Model_Environment, Limitations, Repository_Contents
└── tests/           pytest suite (values + output existence)
```

## Module responsibilities (`src/responsible_llm_audit/`)
| Module | Responsibility |
|---|---|
| `config.py` | locate repo root; load YAML/JSON configuration |
| `io.py` | load & validate source files; typed exceptions |
| `preprocessing.py` | strip `<think>`, build full + 180-word display forms |
| `markers.py` | crisis/disclaimer/cultural marker detection |
| `readability.py` | rule-based FKGL, FRE, sentence length, chars/word |
| `fnmwcf.py` | FNMWCF lexical coverage |
| `keywords.py` | top content tokens (shared stopword pipeline) |
| `personas.py` | persona verification against the CCHS PUMF |
| `prompts.py` | prompt/response accounting |
| `pilot_ratings.py` | exploratory pilot summary |
| `statistics.py` | Wilson CI, Cohen's h, trimming sensitivity |
| `tables.py` | generate all quantitative tables |
| `figures.py` | generate the 7 empirical figures |
| `validation.py` | compare to expected results; check outputs |
| `reproduce.py` | end-to-end orchestration |

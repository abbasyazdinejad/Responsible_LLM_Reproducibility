# Model & Inference Environment

The model generations were produced with the following configuration (recorded from the original study;
these are reported for transparency and are **not** re-run by this repository, which analyses the stored
responses).

## Models
| Display name | Ollama tag | Parameters |
|---|---|---|
| DeepSeek-r1:8B | `deepseek-r1:8b` | 8B (distilled reasoning model) |
| LLaMA-3.2:latest | `llama3.2:latest` | 3B (instruction-tuned) |
| Mistral-7B | `mistral:7b` | 7B (instruction-tuned) |

## Decoding parameters
- temperature = 0.7
- max tokens (num_predict) = 256
- top-p = 0.95
- generations per persona per model = 150 (→ 450 responses per model)
- inference engine: Ollama v0.1.34 (local execution)

## Reproducibility limitation — model checkpoint digests
Model tags such as `llama3.2:latest` are **mutable** and do not uniquely identify a build. **Immutable
model checkpoint digests and quantization settings were NOT recorded for the original runs.** Byte-exact
re-generation therefore cannot be guaranteed; this repository instead ships the **stored model responses**
so that all reported metrics are exactly reproducible from the data. If you re-generate responses with your
own Ollama models, record the digests with `ollama show <tag>` for provenance.

## Analysis environment
- Python ≥ 3.9 (developed on 3.10).
- pandas, numpy, matplotlib, scipy, PyYAML (see `requirements.txt` / `environment.yml`).
- Readability (FKGL) uses a self-contained, rule-based syllable counter — no external corpus (e.g. NLTK
  cmudict) is required, so the pipeline runs fully offline.
- The analysis is deterministic (no sampling, no model inference at analysis time).

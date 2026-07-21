"""Prompt and response accounting."""
from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from .config import Config


def prompt_accounting(prompts: pd.DataFrame, resp: pd.DataFrame, cfg: Config) -> Dict[str, Any]:
    """Return a dict describing the corpus construction.

    The corpus is three predefined persona prompts, each generated 150 times per model.
    """
    gens = prompts.groupby("context").size()
    acct: Dict[str, Any] = {
        "n_prompt_rows": int(len(prompts)),
        "n_unique_personas": int(prompts["context"].nunique()),
        "n_unique_prompt_texts": int(prompts["prompt"].nunique()),
        "generations_per_persona": int(gens.iloc[0]) if gens.nunique() == 1 else gens.to_dict(),
        "responses_per_model": {cfg.model_labels[t]: int((resp["model"] == t).sum())
                                for t in cfg.model_tags},
        "n_responses_total": int(len(resp)),
        "n_empty_responses": int((resp["response"].isna()
                                  | (resp["response"].astype(str).str.strip() == "")).sum()),
        "n_error_responses": int(resp["response"].astype(str).str.startswith("[ERROR]").sum()),
    }
    return acct

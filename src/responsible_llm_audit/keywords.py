"""Top content-token analysis with a single, shared stopword pipeline.

Table 5 (top-5) and Figure 6 (top-10) in the manuscript are produced by the *same*
function here, guaranteeing they are consistent.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import List, Tuple

import pandas as pd

from .config import Config

_TOKEN = re.compile(r"[a-zA-Z']+")


def top_tokens(texts: pd.Series, cfg: Config, n: int | None = None) -> List[Tuple[str, int]]:
    """Return the ``n`` most frequent content tokens after stopword removal."""
    n = n or cfg.top_n_tokens
    stop = cfg.stopwords
    min_len = cfg.min_token_length
    counter: Counter = Counter()
    for text in texts:
        for w in _TOKEN.findall(str(text).lower()):
            if len(w) > min_len and w not in stop:
                counter[w] += 1
    return counter.most_common(n)


def top_tokens_by_model(resp: pd.DataFrame, cfg: Config, text_col: str = "display",
                        n: int | None = None) -> pd.DataFrame:
    """Long-form table of top tokens per model. Columns: ``model, rank, token, count``."""
    rows = []
    for tag in cfg.model_tags:
        g = resp[resp["model"] == tag]
        for rank, (tok, cnt) in enumerate(top_tokens(g[text_col], cfg, n=n), start=1):
            rows.append({"model": cfg.model_labels[tag], "rank": rank,
                         "token": tok, "count": int(cnt)})
    return pd.DataFrame(rows)

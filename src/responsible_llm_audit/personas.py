"""Persona verification against the CCHS PUMF.

The three personas are *predefined* CCHS-consistent profiles. They were **not** sampled
from the CCHS and are **not** statistically representative. If the CCHS PUMF CSV is
present in ``data/raw/``, this module verifies that each profile corresponds to real
respondent records (reporting the match count). If the PUMF is absent, it reports the
documented match counts from ``config/expected_results.json`` and marks the source as
'documented' so the pipeline still runs offline.
"""
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from .config import Config
from .io import load_persona_metadata


def _pumf_path(cfg: Config):
    fname = cfg.settings["data"].get("pumf_filename", "pumf_cchs.csv")
    p = cfg.raw_dir / fname
    return p if p.exists() else None


def verify_personas(cfg: Config) -> pd.DataFrame:
    """Return a table of the three personas and their CCHS match counts.

    Columns: ``province, sex, age_group, depression_severity, life_satisfaction,
    matching_cchs_records, source`` where ``source`` is 'PUMF' or 'documented'.
    """
    personas = load_persona_metadata(cfg)
    expected: Dict[str, Any] = cfg.expected_results.get("persona_verification", {})
    documented: Dict[str, int] = expected.get("matching_records", {})
    var_map = cfg.settings["personas"]["cchs_variable_map"]  # label -> CCHS column
    code_map = cfg.settings["personas"]["code_map"]          # e.g. {"province": {"SK":47,...}}

    pumf = _pumf_path(cfg)
    rows: List[Dict[str, Any]] = []
    cc = None
    if pumf is not None:
        cols = list(var_map.values())
        cc = pd.read_csv(pumf, usecols=cols, low_memory=False)

    for _, r in personas.iterrows():
        key = f"{r['province']}/{r['sex']}/{r['age_group']}"
        rec: Dict[str, Any] = {
            "province": r["province"], "sex": r["sex"], "age_group": r["age_group"],
            "depression_severity": r.get("depression_severity"),
            "life_satisfaction": r.get("life_satisfaction"),
        }
        if cc is not None:
            mask = pd.Series(True, index=cc.index)
            for label, col in var_map.items():
                if label not in code_map:
                    continue
                val = str(r[label])
                code = code_map[label].get(val, val)
                mask &= (cc[col] == code)
            rec["matching_cchs_records"] = int(mask.sum())
            rec["source"] = "PUMF"
        else:
            rec["matching_cchs_records"] = int(documented.get(key, -1))
            rec["source"] = "documented"
        rows.append(rec)
    return pd.DataFrame(rows)

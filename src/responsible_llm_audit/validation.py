"""Validate computed outputs against the expected manuscript values."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from .config import Config
from .figures import EXPECTED_FIGURES
from .markers import marker_rates
from .prompts import prompt_accounting
from .readability import readability_by_model
from .statistics import trimming_sensitivity


@dataclass
class Check:
    name: str
    expected: Any
    observed: Any
    ok: bool
    tol: float = 0.0


@dataclass
class ValidationResult:
    checks: List[Check] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.ok for c in self.checks)

    def add(self, name: str, expected: Any, observed: Any, tol: float = 0.0) -> None:
        try:
            ok = abs(float(observed) - float(expected)) <= tol
        except (TypeError, ValueError):
            ok = observed == expected
        self.checks.append(Check(name, expected, observed, bool(ok), tol))

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([c.__dict__ for c in self.checks])


def validate(resp: pd.DataFrame, prompts: pd.DataFrame, ratings: pd.DataFrame,
             cfg: Config) -> ValidationResult:
    """Compare computed key values against ``config/expected_results.json``."""
    exp = cfg.expected_results
    tol = float(exp.get("tolerance_pct", 1.0)) / 100.0
    res = ValidationResult()

    acct = prompt_accounting(prompts, resp, cfg)
    res.add("total_responses", exp["counts"]["total_responses"], acct["n_responses_total"])
    for lab, n in acct["responses_per_model"].items():
        res.add(f"responses[{lab}]", exp["counts"]["responses_per_model"], n)

    mk_full = marker_rates(resp, cfg, text_col="full_cleaned").set_index("model")
    for lab, vals in exp["crisis_full"].items():
        res.add(f"crisis_full[{lab}]", vals, round(mk_full.loc[lab, "crisis_guidance_rate"], 3), tol)
    for lab, vals in exp["disclaimer"].items():
        res.add(f"disclaimer[{lab}]", vals, round(mk_full.loc[lab, "disclaimer_or_referral_rate"], 3), tol)

    sens = trimming_sensitivity(resp, cfg).set_index("model")
    for lab, vals in exp["crisis_trimmed"].items():
        res.add(f"crisis_trim[{lab}]", vals, round(sens.loc[lab, "crisis_trimmed180_pct"] / 100, 3), tol)

    rd = readability_by_model(resp, cfg, text_col="display").set_index("model")
    for lab, v in exp["fkgl_mean"].items():
        res.add(f"fkgl[{lab}]", v, round(rd.loc[lab, "fkgl_mean"], 2), float(exp.get("fkgl_tol", 0.5)))

    rated = ratings[ratings["accuracy"].notna()]
    res.add("pilot_deepseek_n", exp["pilot_deepseek_n"],
            int((rated["model"] == "deepseek-r1:8b").sum()))
    return res


def check_outputs_present(cfg: Config, table_names: List[str]) -> List[str]:
    """Return a list of problems (missing / empty / NaN-containing outputs)."""
    problems: List[str] = []
    fig_dir = cfg.path("outputs", "figures")
    for f in EXPECTED_FIGURES:
        p = fig_dir / f
        if not p.exists():
            problems.append(f"missing figure: {f}")
        elif p.stat().st_size < 5000:
            problems.append(f"empty figure: {f}")
    tab_dir = cfg.path("outputs", "tables")
    for t in table_names:
        p = tab_dir / t
        if not p.exists():
            problems.append(f"missing table: {t}")
            continue
        df = pd.read_csv(p)
        if len(df) == 0:
            problems.append(f"empty table: {t}")
        if df.isna().any().any():
            problems.append(f"NaN in table: {t}")
    return problems


def write_report(res: ValidationResult, problems: List[str], cfg: Config) -> Path:
    outdir = cfg.output("validation")
    payload: Dict[str, Any] = {
        "all_value_checks_passed": res.passed,
        "n_checks": len(res.checks),
        "n_failed": sum(1 for c in res.checks if not c.ok),
        "output_problems": problems,
        "checks": [c.__dict__ for c in res.checks],
    }
    p = outdir / "validation_report.json"
    p.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    res.to_frame().to_csv(outdir / "validation_checks.csv", index=False)
    return p

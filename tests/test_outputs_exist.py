"""All expected figures and tables exist, are non-empty, and contain no NaNs."""
import pandas as pd
import responsible_llm_audit as rla

EXPECTED_TABLES = [
    "T_markers.csv", "T_readability.csv", "T_fnmwcf_coverage.csv",
    "T_trimming_sensitivity.csv", "T_top_keywords.csv", "T_response_diagnostics.csv",
    "T_pilot_ratings.csv", "T_persona_verification.csv",
]

def test_figures_exist_nonempty(artifacts, cfg):
    fig_dir = cfg.path("outputs", "figures")
    for f in rla.EXPECTED_FIGURES:
        p = fig_dir / f
        assert p.exists(), f"missing figure {f}"
        assert p.stat().st_size > 5000, f"empty figure {f}"

def test_tables_exist_nonempty_no_nan(artifacts, cfg):
    tab_dir = cfg.path("outputs", "tables")
    for t in EXPECTED_TABLES:
        p = tab_dir / t
        assert p.exists(), f"missing table {t}"
        df = pd.read_csv(p)
        assert len(df) > 0, f"empty table {t}"
        assert not df.isna().any().any(), f"NaN in {t}"

def test_no_output_problems(artifacts):
    assert artifacts.problems == [], artifacts.problems

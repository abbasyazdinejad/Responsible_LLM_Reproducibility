"""FNMWCF lexical coverage sanity checks."""
import responsible_llm_audit as rla

def test_coverage_bounds(prepared):
    cov = rla.coverage_by_model(prepared["resp"], prepared["cfg"], text_col="display")
    theme_cols = [c for c in cov.columns if c.startswith("cov_")]
    assert len(theme_cols) == 4
    vals = cov[theme_cols].values
    assert (vals >= 0).all() and (vals <= 100).all()

def test_lexicon_loaded(cfg):
    assert set(cfg.fnmwcf_lexicon) >= {"culture_as_foundation", "community_and_belonging"}

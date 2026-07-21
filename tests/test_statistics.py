"""Statistics helpers: Wilson CI and Cohen's h."""
import responsible_llm_audit as rla

def test_wilson_ci_reasonable():
    lo, hi = rla.wilson_ci(321, 450)   # ~71.3%
    assert lo < 71.3 < hi and 60 < lo and hi < 80

def test_cohen_h_large_for_crisis_gap():
    h = rla.cohen_h(0.996, 0.713)      # LLaMA vs DeepSeek crisis prevalence
    assert h > 0.8   # large effect

def test_marker_wilson_table(prepared):
    t = rla.marker_wilson_table(prepared["resp"], prepared["cfg"]).set_index("model")
    assert t.loc["DeepSeek-r1:8B", "crisis_ci_low"] < 71.3 < t.loc["DeepSeek-r1:8B", "crisis_ci_high"]

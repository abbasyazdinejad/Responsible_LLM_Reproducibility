"""Safety/cultural marker values on the FULL cleaned responses (primary)."""
import responsible_llm_audit as rla

def test_crisis_full_responses(prepared):
    mk = rla.marker_rates(prepared["resp"], prepared["cfg"], text_col="full_cleaned").set_index("model")
    assert abs(mk.loc["DeepSeek-r1:8B", "crisis_guidance_rate"] - 0.713) < 0.015
    assert abs(mk.loc["LLaMA-3.2:latest", "crisis_guidance_rate"] - 0.996) < 0.015
    assert abs(mk.loc["Mistral-7B", "crisis_guidance_rate"] - 0.996) < 0.015

def test_disclaimer_and_cultural(prepared):
    mk = rla.marker_rates(prepared["resp"], prepared["cfg"], text_col="full_cleaned").set_index("model")
    assert abs(mk.loc["DeepSeek-r1:8B", "disclaimer_or_referral_rate"] - 0.002) < 0.01
    assert mk.loc["LLaMA-3.2:latest", "disclaimer_or_referral_rate"] == 0.0
    assert mk.loc["Mistral-7B", "disclaimer_or_referral_rate"] == 0.0
    for m in ["DeepSeek-r1:8B", "LLaMA-3.2:latest", "Mistral-7B"]:
        assert mk.loc[m, "cultural_marker_rate"] == 1.0

def test_trimming_sensitivity(prepared):
    s = rla.trimming_sensitivity(prepared["resp"], prepared["cfg"]).set_index("model")
    assert abs(s.loc["DeepSeek-r1:8B", "crisis_full_pct"] - 71.3) < 1.0
    assert abs(s.loc["DeepSeek-r1:8B", "crisis_trimmed180_pct"] - 30.0) < 1.0
    assert abs(s.loc["LLaMA-3.2:latest", "crisis_trimmed180_pct"] - 97.6) < 1.0
    assert abs(s.loc["Mistral-7B", "crisis_trimmed180_pct"] - 96.9) < 1.0
    # trimming materially affects only DeepSeek
    assert s.loc["DeepSeek-r1:8B", "delta_pts"] > 30
    assert s.loc["LLaMA-3.2:latest", "delta_pts"] < 5

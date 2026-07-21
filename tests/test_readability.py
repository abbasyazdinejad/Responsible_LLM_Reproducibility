"""Readability (FKGL) values on the display responses."""
import numpy as np
import responsible_llm_audit as rla

def test_fkgl_means(prepared):
    rd = rla.readability_by_model(prepared["resp"], prepared["cfg"], text_col="display").set_index("model")
    assert abs(rd.loc["DeepSeek-r1:8B", "fkgl_mean"] - 10.8) < 0.5
    assert abs(rd.loc["LLaMA-3.2:latest", "fkgl_mean"] - 9.8) < 0.5
    assert abs(rd.loc["Mistral-7B", "fkgl_mean"] - 10.4) < 0.5
    # all exceed the grade 6-8 patient-facing band
    assert (rd["fkgl_mean"] > 8).all()

def test_fkgl_deterministic():
    a = rla.flesch_kincaid_grade("This is a simple sentence for testing readability.")
    b = rla.flesch_kincaid_grade("This is a simple sentence for testing readability.")
    assert a == b and not np.isnan(a)

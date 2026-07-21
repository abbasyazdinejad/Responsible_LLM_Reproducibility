"""Validate all computed values against config/expected_results.json."""
import responsible_llm_audit as rla

def test_all_value_checks_pass(prepared):
    res = rla.validate(prepared["resp"], prepared["prompts"], prepared["ratings"], prepared["cfg"])
    failed = [c.name for c in res.checks if not c.ok]
    assert res.passed, f"failed checks: {failed}"

def test_sample_accounting(prepared):
    acct = rla.prompt_accounting(prepared["prompts"], prepared["resp"], prepared["cfg"])
    assert acct["n_responses_total"] == 1350
    assert acct["n_unique_personas"] == 3
    assert all(n == 450 for n in acct["responses_per_model"].values())

def test_pilot_n(prepared):
    s = rla.pilot_summary(prepared["ratings"], prepared["cfg"])
    assert s["deepseek_n"] == 13
    assert s["reliability_computable"] is False

def test_model_names_consistent(cfg):
    assert cfg.ordered_labels == ["DeepSeek-r1:8B", "LLaMA-3.2:latest", "Mistral-7B"]

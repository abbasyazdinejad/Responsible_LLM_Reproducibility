"""Keyword pipeline: function words removed; Table 5 == top-5 of Figure 6 pipeline."""
import responsible_llm_audit as rla

FUNCTION_WORDS = {"your", "with", "that", "this", "they", "have"}

def test_no_function_words(prepared):
    kw = rla.top_tokens_by_model(prepared["resp"], prepared["cfg"], text_col="display", n=10)
    assert not (set(kw["token"]) & FUNCTION_WORDS)

def test_expected_top_tokens(prepared):
    kw = rla.top_tokens_by_model(prepared["resp"], prepared["cfg"], text_col="display", n=10)
    ds = kw[(kw.model == "DeepSeek-r1:8B") & (kw["rank"] <= 5)].token.tolist()
    assert ds == ["support", "community", "wellness", "land", "based"]
    mistral = kw[(kw.model == "Mistral-7B") & (kw["rank"] <= 5)].token.tolist()
    assert "crisis" in mistral

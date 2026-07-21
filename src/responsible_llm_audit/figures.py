"""Generate the seven data-derived empirical figures (written to ``outputs/figures``).

Figures 8-10 in the manuscript are conceptual / methodological diagrams created in the
manuscript itself; they are intentionally NOT produced here.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from .config import Config
from .fnmwcf import coverage_by_model
from .keywords import top_tokens_by_model
from .markers import add_marker_flags, marker_rates
from .pilot_ratings import AXES, pilot_summary
from .readability import readability_by_model

EXPECTED_FIGURES: List[str] = [
    "fig_markers.png", "fig_readability.png", "fig_fnmwcf.png", "fig_length.png",
    "fig_variability.png", "fig_keywords.png", "fig_pilot.png",
]
_PALETTE = {"__default__": ["#4C72B0", "#DD8452", "#55A868"]}


def _colors(labels: List[str]) -> Dict[str, str]:
    base = _PALETTE["__default__"]
    return {lab: base[i % len(base)] for i, lab in enumerate(labels)}


def generate_all_figures(resp: pd.DataFrame, ratings: pd.DataFrame,
                         cfg: Config, outdir: Path | None = None) -> Dict[str, Path]:
    """Render all seven figures. Raises if any figure is empty. Returns {name: path}."""
    outdir = outdir or cfg.output("figures")
    order = cfg.ordered_labels
    col = _colors(order)
    tags = {cfg.model_labels[t]: t for t in cfg.model_tags}
    plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3,
                         "axes.axisbelow": True})
    written: Dict[str, Path] = {}

    def _save(fig, name):
        p = outdir / name
        fig.savefig(p, dpi=300, bbox_inches="tight")
        plt.close(fig)
        if p.stat().st_size < 5000:
            raise RuntimeError(f"Figure {name} is empty / too small.")
        written[name] = p

    # Figure 1: safety & cultural markers (full cleaned responses)
    mk = marker_rates(resp, cfg, text_col="full_cleaned").set_index("model").loc[order]
    x = np.arange(len(order)); w = 0.26
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar(x - w, mk["cultural_marker_rate"] * 100, w, label="Cultural marker (lexical)", color="#55A868")
    ax.bar(x, mk["crisis_guidance_rate"] * 100, w, label="Crisis-guidance language", color="#C44E52")
    ax.bar(x + w, mk["disclaimer_or_referral_rate"] * 100, w, label="Disclaimer / referral", color="#8172B3")
    for i, lab in enumerate(order):
        ax.text(i - w, mk.loc[lab, "cultural_marker_rate"] * 100 + 1.5, f"{mk.loc[lab,'cultural_marker_rate']*100:.0f}%", ha="center", fontsize=8)
        ax.text(i, mk.loc[lab, "crisis_guidance_rate"] * 100 + 1.5, f"{mk.loc[lab,'crisis_guidance_rate']*100:.1f}%", ha="center", fontsize=8)
        ax.text(i + w, mk.loc[lab, "disclaimer_or_referral_rate"] * 100 + 1.5, f"{mk.loc[lab,'disclaimer_or_referral_rate']*100:.1f}%", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(order); ax.set_ylim(0, 108)
    ax.set_ylabel("Responses containing marker (%)")
    ax.set_title("Explicit safety and cultural markers by model, full responses (n=450 per model)")
    ax.legend(fontsize=9, loc="center right")
    _save(fig, "fig_markers.png")

    # Figure 2: readability (FKGL) with recommended band
    rd = readability_by_model(resp, cfg, text_col="display").set_index("model").loc[order]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.bar(order, rd["fkgl_mean"], yerr=rd["fkgl_sd"], capsize=5, color=[col[m] for m in order])
    band = cfg.settings["figures"]["readability_band"]
    ax.axhspan(band[0], band[1], color="tab:green", alpha=0.15, label=f"Recommended (Grade {band[0]}-{band[1]})")
    for i, lab in enumerate(order):
        ax.text(i, rd.loc[lab, "fkgl_mean"] + 0.2, f"{rd.loc[lab,'fkgl_mean']:.1f}", ha="center", fontsize=9)
    ax.set_ylabel("Flesch-Kincaid Grade Level"); ax.set_ylim(0, 14)
    ax.set_title("Readability of model outputs (mean +/- SD across 450 responses)")
    ax.legend(fontsize=9)
    _save(fig, "fig_readability.png")

    # Figure 3: FNMWCF lexical coverage by theme
    cov = coverage_by_model(resp, cfg, text_col="display")
    themes = [c for c in cov.columns if c.startswith("cov_")]
    tlab = [t.replace("cov_", "").replace("_", " ") for t in themes]
    xx = np.arange(len(themes))
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for i, lab in enumerate(order):
        vals = cov.loc[cov.model == lab, themes].values.flatten()
        ax.bar(xx + (i - 1) * w, vals, w, label=lab, color=col[lab])
    ax.set_xticks(xx); ax.set_xticklabels(tlab, fontsize=8); ax.set_ylim(0, 112)
    ax.set_ylabel("Responses with >=1 theme term (%)")
    ax.set_title("FNMWCF lexical coverage by theme (proxy only; not cultural adequacy)")
    ax.legend(fontsize=9, ncol=3, loc="lower center")
    _save(fig, "fig_fnmwcf.png")

    # Figure 4: length + trimming rate
    from .tables import response_diagnostics
    dg = response_diagnostics(resp, cfg).set_index("model").loc[order]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    axes[0].bar(order, dg["mean_words"], color=[col[m] for m in order])
    axes[0].axhline(cfg.display_word_cap, ls="--", color="gray")
    axes[0].set_ylabel("Mean words (display)"); axes[0].set_ylim(0, 200)
    axes[0].set_title(f"Mean response length ({cfg.display_word_cap}-word cap)")
    for i, lab in enumerate(order):
        axes[0].text(i, dg.loc[lab, "mean_words"] + 3, f"{dg.loc[lab,'mean_words']:.0f}", ha="center", fontsize=9)
    axes[1].bar(order, dg["pct_at_180_cap"], color=[col[m] for m in order])
    axes[1].set_ylabel(f"% responses at {cfg.display_word_cap}-word cap"); axes[1].set_ylim(0, 100)
    axes[1].set_title(f"Trimming rate at {cfg.display_word_cap} words")
    for i, lab in enumerate(order):
        axes[1].text(i, dg.loc[lab, "pct_at_180_cap"] + 1.5, f"{dg.loc[lab,'pct_at_180_cap']:.0f}%", ha="center", fontsize=9)
    for ax in axes:
        ax.set_xticks(np.arange(len(order)))
        ax.set_xticklabels(order, rotation=12)
    _save(fig, "fig_length.png")

    # Figure 5: within-model readability variability
    from .readability import flesch_kincaid_grade
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    data = [resp.loc[resp.model == tags[lab], "display"].map(flesch_kincaid_grade).dropna().values
            for lab in order]
    if any(len(d) == 0 for d in data):
        raise RuntimeError("fig_variability: empty FKGL group.")
    try:
        bp = ax.boxplot(data, tick_labels=order, patch_artist=True, showmeans=True)
    except TypeError:  # matplotlib < 3.9
        bp = ax.boxplot(data, labels=order, patch_artist=True, showmeans=True)
    for patch, lab in zip(bp["boxes"], order):
        patch.set_facecolor(col[lab]); patch.set_alpha(0.6)
    ax.set_ylabel("Flesch-Kincaid Grade Level")
    ax.set_title("Readability variability across repeated generations (T = 0.7)", fontsize=12)
    _save(fig, "fig_variability.png")

    # Figure 6: top-10 content tokens (same pipeline as Table 5)
    kw = top_tokens_by_model(resp, cfg, text_col="display", n=10)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
    for ax, lab in zip(axes, order):
        sub = kw[kw.model == lab].sort_values("rank", ascending=False)
        ax.barh(sub["token"], sub["count"], color=col[lab])
        ax.set_title(lab, fontsize=11); ax.set_xlabel("count")
    fig.suptitle("Top-10 content tokens by model (cultural vs. clinical framing)", y=1.02)
    _save(fig, "fig_keywords.png")

    # Figure 7: exploratory single-rater DeepSeek pilot
    ps = pilot_summary(ratings, cfg)
    labels = ["Accuracy", "Cultural\nrelevance", "Language\naccessibility", "Bias\navoidance"]
    means = [ps["deepseek_means"][a] for a in AXES]
    sems = [ps["deepseek_sem"][a] for a in AXES]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.bar(labels, means, yerr=sems, capsize=6, color="#4C72B0", alpha=0.85)
    for i, (m, s) in enumerate(zip(means, sems)):
        ax.text(i, m + s + 0.08, f"{m:.2f}", ha="center", fontsize=9)
    ax.set_ylim(0, 3.2); ax.set_ylabel("Rubric score (0-3)")
    ax.set_title(f"Exploratory single-rater DeepSeek-r1:8B pilot (n={ps['deepseek_n']}, one rater)")
    _save(fig, "fig_pilot.png")

    return written

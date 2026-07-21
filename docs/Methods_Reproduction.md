# Methods (Reproduction Summary)

A concise description of what the pipeline computes; see the manuscript Methods for full context.

1. **Corpus.** Three predefined, CCHS-consistent persona prompts (FNMWCF-informed). Each prompt was sent to
   each model 150 times at temperature 0.7, giving 450 responses per model and 1,350 in total.
2. **Cleaning → two text forms.** `<think>` reasoning traces are removed to form the **full cleaned**
   response; this is then trimmed to a 180-word **display** response. The 256-token generation cap and the
   180-word display cap are distinct.
3. **Safety & cultural markers.** Fixed regular expressions (`config/marker_patterns.json`) detect
   crisis-guidance language, disclaimers/referrals, and cultural terms on the **full cleaned** responses
   (because markers concern whether guidance was provided at all). Proportions are reported with Wilson 95%
   confidence intervals, conditional on the three fixed personas and repeated generations.
4. **Trimming sensitivity.** Crisis-marker prevalence is compared between the full and display forms.
5. **Readability.** Sentence length, characters/word, and a self-contained Flesch–Kincaid Grade Level on
   the **display** responses.
6. **FNMWCF lexical coverage.** A published theme lexicon (`config/fnmwcf_lexicon.json`); a proxy only, not
   a measure of cultural adequacy.
7. **Keyword framing.** Top content tokens after standard stopword removal (identical pipeline for the
   table and the figure).
8. **Exploratory pilot.** A single-rater 0–3 rubric pilot (DeepSeek n=13); inter-rater reliability is not
   computable with a single rater.
9. **Statistics.** Descriptive only: proportions with Wilson CIs and Cohen's h effect sizes. No inferential
   hypothesis tests are performed, so no multiple-comparison correction is applicable.

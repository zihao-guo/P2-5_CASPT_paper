# Conference conversion: source and material map

The authoritative source is `res/P2_5_Zihao_2026_CAIEVERSION.zip`, especially `cas-sc-template.tex` and `cas-refs.bib`. `main.tex` is the conference paper; its `\rev{zg}{old}{new}` commands identify marked wording changes, and `\keepcomment` is set to 1 by default to display them. The original abstract is retained in the old argument; selected omitted introduction and conclusion sentences are also marked as deletions (their original citation keys are retained in nearby source comments). The official template changes, moved sections, and every passage omitted for space are not all shown as deletions: consult the archive for the complete wording. This map identifies where the principal technical material can be found and does not replace a line-by-line diff.

| Original material | Conference paper | Supplement |
| --- | --- | --- |
| Introduction and related-work discussion | Introduction, condensed | Additional related work reproduces the literature discussion and comparison table; the original introduction remains in the archive |
| Network, passenger assignment, objectives and constraints | Methodology, including compact constraints | Framework figure and detailed line-structure and fleet constraints; original full derivation remains in the archive |
| Encoding, initialization, crossover, mutation and selection | Solution algorithm, condensed | Additional details of the solution algorithm, including the original NSGA-III pseudocode and decode-and-assign evaluation |
| Log-normal travel times and prediction errors | Evaluation method | Stochastic modelling of travel times and prediction errors, including prediction-error data |
| Mandl aggregate and frequency-only results | Full five-line-count table, Pareto-front plot and single-realization distributions | Full result table, distributions, and OD-level exceedance plots |
| Forecast-error sensitivity | Evaluation and results, condensed | Forecast-value metrics and results |
| Beijing results | High-variability baseline table and redesign table | Full skip-threshold table and original and adapted network visualisations |
| Temporal stability proof and performance metrics | Structural continuity objective and metrics, condensed | Pairwise stability proof; network and multi-objective performance metrics |
| Conclusion and limitations | Conclusion, condensed | Original full wording remains in the archive |

Table values reproduced from the source have not been regenerated from the experimental code in this conversion. The conference manuscript distinguishes the unweighted Beijing OD travel-time aggregate from a demand-weighted metric, following the explicit formula in the original source. The rolling trigger is presented as a possible deployment rule, not as a validated multi-hour experiment.

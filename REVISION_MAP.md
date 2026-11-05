# Conference conversion: source and material map

The authoritative source is `res/P2_5_Zihao_2026_CAIEVERSION.zip`, especially `cas-sc-template.tex` and `cas-refs.bib`. `main.tex` is the conference paper; its `\rev{zg}{old}{new}` commands identify marked wording changes, and `\keepcomment` is set to 1 by default to display them. The original abstract is retained in the old argument; selected omitted introduction and conclusion sentences are also marked as deletions (their original citation keys are retained in nearby source comments). The official template changes, moved sections, and every passage omitted for space are not all shown as deletions: consult the archive for the complete wording. This map identifies where the principal technical material can be found and does not replace a line-by-line diff.

| Original material | Conference paper | Supplement |
| --- | --- | --- |
| Introduction and related-work discussion | Introduction, condensed | Additional related work reproduces the literature discussion and comparison table; the original introduction remains in the archive |
| Network, passenger assignment, objectives and constraints | Methodology, including compact constraints | Line travel-time, headway and waiting-time equations, virtual-node transfer model and figure, original shortest-path assignment observation, framework figure, and detailed line-structure and fleet constraints |
| Encoding, initialization, crossover, mutation and selection | Solution algorithm, condensed | Additional details of the solution algorithm, including the original NSGA-III pseudocode and decode-and-assign evaluation |
| Log-normal travel times and prediction errors | Evaluation method | Stochastic modelling of travel times and prediction errors, including prediction-error data |
| Mandl aggregate and frequency-only results | Full five-line-count table, Pareto-front plot and single-realization distributions | Full result and frequency-only comparison tables, distributions, and OD-level exceedance plots |
| Forecast-error sensitivity | Evaluation and results, condensed | Forecast-value metrics and results |
| Beijing results | High-variability baseline table and redesign table | Full skip-threshold table and original and adapted network visualisations |
| Temporal stability proof and performance metrics | Structural continuity objective and metrics, condensed | Pairwise stability proof; network and multi-objective performance metrics |
| Conclusion and limitations | Conclusion, condensed | Original full wording remains in the archive |

Table values reproduced from the source have not been regenerated from the experimental code in this conversion. The conference manuscript distinguishes the unweighted Beijing OD travel-time aggregate from a demand-weighted metric, following the explicit formula in the original source. The rolling trigger is presented as a possible deployment rule, not as a validated multi-hour experiment.

`python3 scripts/check-result-tables.py` compares the 75 Mandl mean/standard-deviation entries, 24 frequency-only comparison entries and decimal-valued Beijing table entries against the archived LaTeX source. It checks transcription only, not the underlying experimental computations or the original table’s use of dashes for redesign connectivity.

The source gives conflicting descriptions of the OD-improvement exceedance figure: its main explanation describes pointwise averaging over seeds, while its caption describes trimming extreme curves before averaging. A search of the current workspace and the original archive found image files but no matching plotting code or raw result data; the thesis repeats both conflicting descriptions. The supplement therefore identifies this uncertainty instead of asserting either aggregation.

The conference Pareto-front image and both single-realization travel-time distribution images are byte-identical (SHA-256) to their counterparts in the source archive; their data and plots have not been regenerated.

The conference title, author order, affiliations, corresponding author and email addresses were checked against `title_page.tex` in the source archive. The title page in the original manuscript itself is anonymized, while the conference template requests author details.

All nonempty OLD spans match their claimed source locations. Retained numerical values, rounding, captions, and equation bodies match. The mock has eight A4 pages, a 92-word abstract, five keywords, and no unresolved labels or citation keys.

Line numbers below refer to the original manuscript unless otherwise specified.

- **[MAJOR] Unmarked header deletions** — Table 2, draft L360 — original L1664–1670 — Seven header cells lose explanatory text, including “Skip threshold” and “Line Overlap (\%).” These are textual deletions, not merely float scaffolding. **Fix:** restore those headers or mark each deleted span with `\rev{cc}{OLD}{}`.

- **[MAJOR] Unsupported edge-set equality** — M-2a+, “`\pazocal{E}=\pazocal{E}^{\text{sub}}`” — original L473, L593 — The source describes the latter as all potential connections, but defines the former as “feasible edges.” Their equality is not established. **Fix:** replace the inserted sentence with `\rev{cc}{}{Let $\pazocal{E}$ denote the set of feasible edges in the network.}`

- **[MAJOR] Incorrect percentage units** — Table 2 note, “All values are in \%” — original L1665–1670, L1704 — CV is dimensionless: 1.00 means a coefficient of variation of one, not 1%. **Fix:** change that sentence inside its existing insertion to “All performance metrics are percentages; CV is dimensionless.”

- **[MAJOR] Forecast robustness loses its qualification** — R-8c, “When variability is high … changes little when varying … $\alpha$” — original L1624, L2390, L2409 — The rewritten antecedent is faithful, but the retained standalone claim omits the appendix’s deterioration under severe amplification. Evidence specifically supports empirical error and moderate amplification, $\alpha=1.5$. **Fix:** add inside the existing marked parenthesis: “for empirical and moderately amplified errors; severe amplification degrades performance.”

- **[MAJOR] Essential limits disappear** — M-3d and conclusion’s “performance … severe traffic fluctuations” — original L666–667, L718 — The draft removes both uncongested passenger assignment and the operational-feasibility caveat. Fleet limits do not communicate the exclusion of capacity and crowding. **Fix:** restore candidates 1 and 4 below.

- **[MAJOR] OD-cost and connectivity explanations are incomplete** — M-3e, “sum of the predicted link times”; A-3a, “in-vehicle travel times and waiting times” — original L503–505, L671, L1019–1030, L1279 — Fixed transfer penalties and the one-minute dwell assumption disappear; the claimed full connectivity also loses its initialization screening explanation. **Fix:** add marked text specifying all OD-cost components, the 5-minute transfer penalty, one-minute dwell time, and the OD-connectivity screening. The new one-way `\hat t^\ell` definition and simple-path/fleet constraint summary themselves are supported by L562–575 and L817–868.

- **[MAJOR] Stop-skipping TTI denominator becomes unclear** — R-10, “across all OD pairs,” alongside finite Table 2 TTI and disconnected ODs — original L1737–1740, L1746, L1748 — The removed discussion specifies improvements on the reachable network for stop-skipping, versus full-demand coverage for redesign. **Fix:** restore candidate 3 and explicitly qualify the stop-skipping evaluation set.

- **[MAJOR] Error sampling is underdefined** — E-4, “empirical logarithmic prediction errors” — original L1170–1181; `pred_error.tex` L32, L45–52 — The log-relative definition, pooling, and independent sampling with replacement are missing. **Fix:** insert the definition `$\eta=\log(\hat t/t)=\log(v/\hat v)$`, defining both speeds, and restore candidate 2.

- **[MINOR] Mandl wording now covers Beijing** — E-2, “the Mandl’s dataset” — original L1146, L1216; `pred_error.tex` L50 — The shared evaluation section incorrectly restricts nominal times to Mandl. **Fix:** `\rev{cc}{the Mandl's dataset}{the corresponding network dataset}`.

- **[MINOR] Fallback creates a dangling enumeration** — plan A cuts R-12c first, retaining “two structural reasons” and “First” — original L1748 — Only one reason would remain. **Fix:** accompany that cut with `\rev{cc}{two structural reasons}{a structural reason}` and `\rev{cc}{First, it}{It}`.

- **[MINOR] Definitions disappear** — abstract “NSGA-III”; M-3d “$\omega\in\Omega$” — original L199, L539 — Neither acronym expansion nor $\Omega$’s definition survives. **Fix:** restore the expansion and insert a marked definition of the realization space.

- **[MINOR] Template/reference defects** — unnumbered stability display and narrative citations rendering “used by Mandl, 1980” — original L758–760, L391, L1277–1280; template L222–223, L272 — **Fix:** number the display; replace narrative `\cite` calls with marked `\citet` replacements.

### Restore candidates

In priority order:

1. **L666–667:** “Accordingly, when computing shortest paths we assume links are uncongested: link travel times are exogenous to passenger volumes, so the reported trip times are user-optimal times that abstract away vehicle capacity and in-vehicle crowding (a redesigned line is never penalized for the demand it attracts).”
2. **`pred_error.tex` L50:** “Finally, independent samples $\eta_{ij}^{\omega}$ are drawn with replacement from this empirical pool for each link $(i,j)$ and scenario $\omega$.”
3. **L1746:** “Aggressive thresholds improve travel time on the reachable network but disconnect a large share of OD pairs as variability grows, whereas conservative thresholds keep connectivity yet act too rarely to help and still lose connectivity at high variability.”
4. **L718:** “The operational feasibility of these assumptions—one-hour advance notice, predefined deviation zones, and app-based passenger guidance—is therefore context-dependent.”

VERDICT: PLAN OK WITH FIXES.

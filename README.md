# P2-5_CASPT_paper

Research-track submission to **CASPT & TransitData 2027** (Stockholm, 21–24 June 2027):
*Predict-then-Optimize Framework for Public Transport Line Redesign under Fluctuating Traffic Conditions*.

The paper is a condensed version (8 pages maximum, references included) of the journal-length
manuscript in `res/P2_5_Zihao_2026_CAIEVERSION/`. Everything that does not fit — appendices, proofs,
algorithmic details, additional experiments — is referred to as the **extended report**
(`\citep{guo2026extended}`), to be posted on arXiv.

## Layout

| Path | What it is |
|---|---|
| `main.tex` | The paper, in the official CASPT2027 LaTeX template (deviations from the template preamble are tagged `CASPT-ADAPT`). |
| `bibliography.bib` | The cited subset of the original `cas-refs.bib` plus the extended-report entry. |
| `main_clean.pdf` | Submission version (revision marks hidden, `\keepcomment=0`). |
| `main_marked.pdf` | Marked version (`\keepcomment=1`): what differs from the original manuscript. |
| `extended_report/` | arXiv-ready extended report: the full original manuscript with title suffix, author block and a first-page note (`extended_report.tex`, compiled PDF, `.bbl`). |
| `res/` | The original manuscript, unmodified (reference for all checks). |
| `build.sh` | Builds both PDFs and fails if either exceeds 8 pages. |
| `tools/` | `check_verbatim.py` (fidelity check), `make_orig_labels.py`, `prune_bib.py`. |
| `orig_labels.tex` | Original label numbers, used only inside struck-out old text of the marked version. |
| `qa/` | Codex (`gpt-6-astra`, xhigh) review of each modification step, with what was done about each finding. |

## Building

```bash
./build.sh          # pdflatex + biber (biblatex-apa); writes main_clean.pdf and main_marked.pdf
```

`main.tex` itself is compiled as-is by any LaTeX editor; `\newcommand{\keepcomment}{1}` shows the marks,
`{0}` gives the submission version.

## Revision-mark convention

- Text is taken **verbatim** from the original manuscript wherever possible.
- Anything that differs inside a kept sentence, and every newly written sentence, is wrapped as
  `\rev{cc}{old}{new}` (`old` = exact original text, `new` = replacement; either may be empty).
- Whole sentences, paragraphs, sections, floats and table rows that were left out are **not** marked
  (they are in the extended report); the marked PDF would otherwise be as long as the original.
- Layout-only adaptations to the template are not marked either: float placement options, table
  captions above tables, the numbered display in the stability proposition, row spacing in the
  objective equation and in the tables, and the scaling of the Beijing table to the text width.

`tools/check_verbatim.py` enforces this: with every `\rev{cc}{old}{new}` replaced by `old`, all body text
must match the original token for token.

```bash
python3 tools/check_verbatim.py --orig res/P2_5_Zihao_2026_CAIEVERSION/cas-sc-template.tex --new main.tex
```

## To do before submission (authors)

- Post `extended_report/` on arXiv and replace the placeholder `XXXX.XXXXX` in `bibliography.bib`
  (entry `guo2026extended`).
- Confirm the affiliation of the third author (the original `title_page.tex` and the commented author
  block of the manuscript disagree; `title_page.tex` was followed).
- Set `\keepcomment` to `0` (or use `main_clean.pdf`) for the EasyChair upload.

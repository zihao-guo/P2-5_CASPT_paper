# P3_ACC_CASPT_paper

Research-track submission to **CASPT & TransitData 2027** (Stockholm, 21–24 June 2027):
*Proactive–Adaptive Public Transport Planning: Bus Network Redesign for Urban Rail Disruptions*.

Condensed from the WCTR 2026 manuscript (`res/WCTR2026/TRPRO_WCTR 2026..tex`, unmodified copy of
`P3_Zihao_2025_WCTR2026.zip`) into the official CASPT2027 LaTeX template.

CASPT requirements followed (https://www.caspt-transitdata2027.conf.kth.se/call-for-papers):
research track, **up to 8 pages**, official template, EasyChair submission, deadline 16 October 2026.

| Path | What it is |
|---|---|
| `main.tex` | The paper (CASPT2027 template preamble; deviations tagged `CASPT-ADAPT`). |
| `bibliography.bib` | Cited subset of the original `xampl.bib`. |
| `Figure/` | Figures from the original manuscript. |
| `main.pdf` | Compiled paper. |
| `build.sh` | pdflatex + biber; fails if `main.pdf` exceeds 8 pages. |
| `res/WCTR2026/` | Original manuscript package (reference only). |

Left out for space (still in the original): the separate related-work section (merged into the
introduction), the notation tables, the full path-structure / node-access constraint listings and
their linearizations (summarized in words).

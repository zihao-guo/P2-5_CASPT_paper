#!/usr/bin/env python3
"""Compare the conference result tables against the archived source."""
from pathlib import Path
import re
from zipfile import ZipFile

root = Path(__file__).resolve().parent.parent
with ZipFile(root / "res/P2_5_Zihao_2026_CAIEVERSION.zip") as archive:
    name = next(n for n in archive.namelist() if n.endswith("cas-sc-template.tex"))
    original = archive.read(name).decode("utf-8")
paper = (root / "main.tex").read_text()

start = original.index(r"\multirow{3}{*}{\textbf{4}}", original.index(r"\label{tab:routeNumberCV}") - 5000)
original_table = original[start:original.index(r"\bottomrule", start)]
start = paper.index(r"\multirow{3}{*}{\textbf{4}}")
conference_table = paper[start:paper.index(r"\bottomrule", start)]
pattern = r"\$(\d+\.\d+\\pm\d+\.\d+)\$"
original_values = re.findall(pattern, original_table)
conference_values = [mean + r"\pm" + std for mean, std in re.findall(
    r"\\meanstd\{(\d+\.\d+)\}\{(\d+\.\d+)\}", conference_table
)]
if len(original_values) != 75 or original_values != conference_values:
    raise SystemExit("Mandl table differs from archived values or has missing entries")

frequency_start = original.index(r"\multirow{3}{*}{\textbf{Frequency Only}}")
frequency_end = original.index(r"\bottomrule", frequency_start)
supplement = (root / "suppl/main.tex").read_text()
supp_start = supplement.index(r"\multirow{3}{*}{\textbf{Frequency Only}}")
supp_end = supplement.index(r"\bottomrule", supp_start)
frequency_values = re.findall(pattern, original[frequency_start:frequency_end])
supp_values = re.findall(pattern, supplement[supp_start:supp_end])
if len(frequency_values) != 24 or frequency_values != supp_values:
    raise SystemExit("Frequency-only comparison table differs from the archived values")

source_start = original.index(r"\multirow{15}{*}{\makecell[c]{Stop-skip.}}")
source_end = original.index(r"\bottomrule", source_start)
source_table = original[source_start:source_end]
rows = re.findall(r"&\s*(?:0\.00|0\.05|0\.25|0\.50|1\.00)\s*&\s*([^\n]+)", source_table)
if len(rows) != 20:
    raise SystemExit(f"Expected 20 Beijing source rows, found {len(rows)}")
def numbers(row):
    return re.findall(r"(?<![\w.])-?\d+\.\d+", row)
source_rows = [numbers(row) for row in rows]
start = paper.index(r"\label{tab:beijing}")
end = paper.index(r"\end{tabular}", start)
short = paper[start:end]
for label, index in [("25", 4), ("50", 9), ("100", 14)]:
    match = re.search(r"Stop-skipping, " + label + r"\\% threshold\s*&([^\n]+)", short)
    if not match or numbers(match.group(1)) != source_rows[index][:4]:
        raise SystemExit(f"Beijing {label}% high-variability row differs from archive")
match = re.search(r"Redesign\s*&([^\n]+)", short)
if not match or numbers(match.group(1)) != source_rows[19][:3]:
    raise SystemExit("Beijing high-variability redesign row differs from archive")
start = paper.index(r"\label{tab:beijing_cvs}")
end = paper.index(r"\end{tabular}", start)
conference = paper[start:end]
for row_name, column in [("Line overlap", 0), ("Operational cost reduction", 1), ("Average travel-time improvement", 2)]:
    match = re.search(re.escape(row_name) + r"\s*\(\\%\)\s*&([^\n]+)", conference)
    expected = [row[column] for row in source_rows[15:20]]
    if not match or numbers(match.group(1)) != expected:
        raise SystemExit(f"Beijing {row_name} row differs from archive")
print("Verified 75 Mandl entries, 24 frequency comparison entries, and the decimal-valued Beijing entries against the archived source.")

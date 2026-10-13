#!/usr/bin/env bash
# Build main.pdf (pdflatex -> biber -> pdflatex x2) and enforce the CASPT
# research-track limit of 8 pages.
cd "$(dirname "$0")" || exit 1
mkdir -p build
log=build/main.log.txt; : > "$log"
step() {
  echo "### $*" >> "$log"
  if ! "$@" >> "$log" 2>&1; then
    echo "FAILED: $* (last 30 lines of $log)"; tail -n 30 "$log"; exit 1
  fi
}
step pdflatex -interaction=nonstopmode -halt-on-error main
step biber main
step pdflatex -interaction=nonstopmode -halt-on-error main
step pdflatex -interaction=nonstopmode -halt-on-error main
info=$(pdfinfo main.pdf)
pages=$(echo "$info" | awk '/^Pages:/{print $2}')
size=$(echo "$info" | sed -n 's/^Page size: *//p')
undef=$(grep -c 'undefined' main.log)
over=$(grep -c 'Overfull \\hbox' main.log)
echo "main.pdf: $pages pages, $size, undefined refs/cites: $undef, overfull hboxes: $over"
if [ "$pages" -gt 8 ]; then echo "PAGE LIMIT EXCEEDED: $pages > 8"; exit 2; fi

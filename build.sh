#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
mkdir -p build

# run_build <jobname>: pdflatex -> biber -> pdflatex x2; prints summary line
run_build() {
  local job="$1" log="build/$1.log.txt"
  : > "$log"
  step() {
    echo "### $*" >> "$log"
    if ! "$@" >> "$log" 2>&1; then
      echo "FAILED: $* (last 30 lines of $log)"; tail -n 30 "$log"; exit 1
    fi
  }
  step pdflatex -interaction=nonstopmode -halt-on-error "$job"
  step biber "$job"
  step pdflatex -interaction=nonstopmode -halt-on-error "$job"
  step pdflatex -interaction=nonstopmode -halt-on-error "$job"
  local info pages size undef over
  info=$(pdfinfo "$job.pdf")
  pages=$(echo "$info" | awk '/^Pages:/{print $2}')
  size=$(echo "$info" | sed -n 's/^Page size: *//p')
  undef=$(grep -c 'undefined' "$job.log")
  over=$(grep -c 'Overfull \\hbox' "$job.log")
  echo "$job.pdf: $pages pages, $size, undefined refs/cites: $undef, overfull hboxes: $over"
}

forced() {  # forced <0|1> <jobname>
  local n
  n=$(grep -c '^\\newcommand{\\keepcomment}{[01]}' main.tex)
  if [ "$n" != "1" ]; then
    echo "ERROR: expected exactly one \\newcommand{\\keepcomment}{0|1} line in main.tex, found $n"; exit 1
  fi
  sed "s/^\\\\newcommand{\\\\keepcomment}{[01]}/\\\\newcommand{\\\\keepcomment}{$1}/" main.tex > "$2.tex"
  run_build "$2"
  rm -f "$2.tex"
}

run_build main
forced 0 main_clean
forced 1 main_marked

rc=0
for f in main_clean main_marked; do
  p=$(pdfinfo "$f.pdf" | awk '/^Pages:/{print $2}')
  if [ "$p" -gt 8 ]; then echo "PAGE LIMIT EXCEEDED: $f.pdf has $p pages"; rc=2; fi
done
exit $rc

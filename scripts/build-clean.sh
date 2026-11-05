#!/bin/sh
# Build clean PDFs without changing the default visible-revision sources.
set -eu
project_dir=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
case ${1:-all} in
  main|supplement|all) target=${1:-all} ;;
  *) printf 'Usage: %s [main|supplement|all]\n' "$0" >&2; exit 2 ;;
esac
build_one() (
  source_dir=$1
  destination=$2
  page_limit=$3
  temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/caspt-clean.XXXXXXXX")
  trap 'rm -rf "$temp_dir"' EXIT HUP INT TERM
  if ! grep -Fq '\newcommand{\keepcomment}{1}' "$source_dir/main.tex"; then
    printf 'Expected keepcomment=1 in %s/main.tex\n' "$source_dir" >&2
    exit 1
  fi
  sed 's/\\newcommand{\\keepcomment}{1}/\\newcommand{\\keepcomment}{0}/' "$source_dir/main.tex" > "$temp_dir/clean-build.tex"
  cd "$source_dir"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$temp_dir" "$temp_dir/clean-build.tex"
  if [ "$page_limit" -gt 0 ]; then
    pages=$(pdfinfo "$temp_dir/clean-build.pdf" | awk '/^Pages:/ {print $2}')
    if [ -z "$pages" ] || [ "$pages" -gt "$page_limit" ]; then
      printf 'Clean conference PDF exceeds %s pages (actual: %s)\n' "$page_limit" "${pages:-unknown}" >&2
      exit 1
    fi
  fi
  mkdir -p "$source_dir/build/clean"
  cp -R "$temp_dir"/. "$source_dir/build/clean/"
  cp "$temp_dir/clean-build.pdf" "$destination"
  printf 'Updated %s\n' "$destination"
)
if [ "$target" = main ] || [ "$target" = all ]; then
  build_one "$project_dir" "$project_dir/submission.pdf" 8
fi
if [ "$target" = supplement ] || [ "$target" = all ]; then
  build_one "$project_dir/suppl" "$project_dir/suppl/clean.pdf" 0
fi

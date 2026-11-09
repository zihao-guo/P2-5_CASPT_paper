#!/bin/sh
# Compile on local temporary storage, then publish the complete build to outDir.
# This avoids pdfTeX's repeated writes to a cloud-synchronised file.
set -eu
source_file=$1
output_dir=$2
source_dir=$(dirname "$source_file")
source_name=$(basename "$source_file")
mkdir -p "$output_dir"
temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/caspt-latex.XXXXXXXX")
trap 'rm -rf "$temp_dir"' EXIT HUP INT TERM
cd "$source_dir"
latexmk -pdf -interaction=nonstopmode -halt-on-error -synctex=1 -file-line-error -outdir="$temp_dir" "$source_name"
cp -R "$temp_dir"/. "$output_dir"/

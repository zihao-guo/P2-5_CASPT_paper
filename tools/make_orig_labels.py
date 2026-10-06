#!/usr/bin/env python3
"""Generate orig_labels.tex from the original manuscript's .aux file.

Usage: make_orig_labels.py <path/to/original.aux> <output.tex>
"""
import re
import sys


def first_group(s, i):
    """s[i] must be '{'; return (content, index after closing brace)."""
    assert s[i] == "{"
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    raise ValueError("unbalanced braces")


def main(aux, out):
    lines = []
    with open(aux, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("\\newlabel{"):
                continue
            try:
                key, i = first_group(line, len("\\newlabel"))
                if i >= len(line) or line[i] != "{":
                    continue
                inner_start = i
                body, _ = first_group(line, inner_start)
                if not body.startswith("{"):
                    continue
                num, _ = first_group(body, 0)
            except (ValueError, AssertionError):
                continue
            if "@" in key or not num.strip():
                continue
            lines.append("\\revoldlabel{%s}{%s}" % (key, num))
    with open(out, "w", encoding="utf-8") as f:
        f.write("% AUTO-GENERATED from the original manuscript's .aux by tools/make_orig_labels.py.\n"
                "% Maps each label of the original manuscript to the number it had there.\n"
                "% Do not edit by hand.\n")
        f.write("\n".join(lines) + "\n")
    print("%d labels written to %s" % (len(lines), out))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

#!/usr/bin/env python3
"""Verbatim-text checker for a condensed LaTeX paper (see module-level helpers)."""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

REV_RE = re.compile(r'\\rev(?=\s*\{)')
HEADING_RE = re.compile(r'^\s*\\(?:(?:sub)*section|paragraph)\b')
INPUT_RE = re.compile(r'\\input\{([^}]*)\}')


# ---------------------------------------------------------------- helpers
def _cut_comment(line):
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c == '\\':
            i += 2
            continue
        if c == '%':
            return line[:i]
        i += 1
    return line


def strip_comments_ln(text):
    """Strip comments line by line; return (text, per-char 1-based line numbers)."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    parts = text.split('\n')
    out = []
    lns = []
    for idx, line in enumerate(parts, 1):
        cut = _cut_comment(line)
        out.append(cut)
        lns.extend([idx] * len(cut))
        if idx < len(parts):
            lns.append(idx)
    return '\n'.join(out), lns


def strip_comments(text):
    return strip_comments_ln(text)[0]


def _match_brace(text, pos):
    """text[pos]=='{'; return index of matching '}' or -1."""
    depth = 0
    i = pos
    n = len(text)
    while i < n:
        c = text[i]
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def parse_rev(text, p):
    """Parse three groups starting at p (just after '\\rev').
    Return ([(a,b)]*3 content spans, end_index) or None."""
    spans = []
    n = len(text)
    for _ in range(3):
        while p < n and text[p].isspace():
            p += 1
        if p >= n or text[p] != '{':
            return None
        q = _match_brace(text, p)
        if q < 0:
            return None
        spans.append((p + 1, q))
        p = q + 1
    return spans, p


def _odd_backslashes_before(text, i):
    k = 0
    while i - 1 - k >= 0 and text[i - 1 - k] == '\\':
        k += 1
    return k % 2 == 1


def _resolve(text, lines, which):
    out = []
    olns = []
    pos = 0
    idx = 1 if which == "old" else 2
    while True:
        m = REV_RE.search(text, pos)
        if not m:
            break
        if _odd_backslashes_before(text, m.start()):
            out.append(text[pos:m.end()])
            olns.extend(lines[pos:m.end()])
            pos = m.end()
            continue
        parsed = parse_rev(text, m.end())
        if parsed is None:
            out.append(text[pos:m.end()])
            olns.extend(lines[pos:m.end()])
            pos = m.end()
            continue
        spans, end = parsed
        a, b = spans[idx]
        sub, _ = _resolve(text[a:b], lines[a:b], which)
        rl = lines[m.start()]
        out.append(text[pos:m.start()])
        olns.extend(lines[pos:m.start()])
        out.append(sub)
        olns.extend([rl] * len(sub))
        pos = end
    out.append(text[pos:])
    olns.extend(lines[pos:])
    return ''.join(out), olns


def resolve_rev_ln(text, lines, which):
    return _resolve(text, lines, which)


def resolve_rev(text, which):
    return _resolve(text, [0] * len(text), which)[0]


def tokenize_ln(text, lines):
    toks = []
    tl = []
    for m in re.finditer(r'\S+', text):
        toks.append(m.group(0))
        tl.append(lines[m.start()])
    return toks, tl


# ---------------------------------------------------------------- original
def load_orig_file(path, depth=0, seen=None):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            raw = f.read()
    except OSError:
        return None
    text = strip_comments(raw)
    if depth > 10:
        return text
    base = os.path.dirname(os.path.abspath(path))

    def sub(m):
        p = m.group(1).strip()
        if not p.lower().endswith('.tex'):
            p += '.tex'
        full = os.path.join(base, p)
        if os.path.isfile(full):
            inner = load_orig_file(full, depth + 1)
            if inner is not None:
                return '\n' + inner + '\n'
        return m.group(0)

    return INPUT_RE.sub(sub, text)


def build_orig_tokens(orig, extras):
    text = load_orig_file(orig)
    if text is None:
        sys.exit("cannot read original file: %s" % orig)
    for e in extras or []:
        t = load_orig_file(e)
        if t is None:
            sys.exit("cannot read extra file: %s" % e)
        text += '\n' + t
    text = resolve_rev(text, "new")
    return text.split()


# ---------------------------------------------------------------- new side
def read_new(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        raw = f.read().replace('\r\n', '\n').replace('\r', '\n')
    lines = raw.split('\n')
    regions = []
    out_lines = []
    in_region = False
    start = 0
    count = 0
    for i, line in enumerate(lines, 1):
        if not in_region and '%%NOCHECK-BEGIN' in line:
            in_region = True
            start = i
            count = 0
            out_lines.append('')
            continue
        if in_region:
            if '%%NOCHECK-END' in line:
                in_region = False
                regions.append((start, i, count))
            else:
                count += len(strip_comments(line).split())
            out_lines.append('')
            continue
        out_lines.append(line)
    if in_region:
        regions.append((start, len(lines), count))
    stripped, lns = strip_comments_ln('\n'.join(out_lines))
    b = stripped.find('\\begin{document}')
    b = 0 if b < 0 else b + len('\\begin{document}')
    e = stripped.rfind('\\end{document}')
    if e < 0 or e < b:
        e = len(stripped)
    return stripped[b:e], lns[b:e], regions, stripped.split('\n')


def find_top_revs(text, lines):
    res = []
    pos = 0
    while True:
        m = REV_RE.search(text, pos)
        if not m:
            break
        if _odd_backslashes_before(text, m.start()):
            pos = m.end()
            continue
        parsed = parse_rev(text, m.end())
        if parsed is None:
            pos = m.end()
            continue
        spans, end = parsed
        g = [text[a:b] for a, b in spans]
        res.append((lines[m.start()], g[0].strip(), g[1], g[2]))
        pos = end
    return res


def abstract_words(text):
    i = text.find('\\textbf{Abstract}')
    if i < 0:
        return None
    i += len('\\textbf{Abstract}')
    j = text.find('\\textbf{Keywords}', i)
    if j < 0:
        return None
    s = text[i:j].lstrip()
    if s.startswith(':'):
        s = s[1:]
    s = re.sub(r'\\([%&_#$])', r'\1', s)
    s = re.sub(r'\\[A-Za-z]+\*?', '', s)
    s = s.replace('{', '').replace('}', '').replace('~', ' ').replace('$', '')
    return len(s.split())


# ---------------------------------------------------------------- matching
def match(O, N, k):
    index = defaultdict(list)
    for p in range(len(O) - k + 1):
        index[tuple(O[p:p + k])].append(p)
    covered = [False] * len(N)
    segs = []
    i = 0
    nn = len(N)
    no = len(O)
    while i < nn:
        best = 0
        bestp = -1
        if i + k <= nn:
            for p in index.get(tuple(N[i:i + k]), ()):
                L = k
                while i + L < nn and p + L < no and N[i + L] == O[p + L]:
                    L += 1
                if L > best:
                    best, bestp = L, p
        if best >= k:
            for t in range(i, i + best):
                covered[t] = True
            segs.append((i, best, bestp))
            i += best
        else:
            i += 1
    return covered, segs


def is_scaffold_token(t):
    return '\\' in t or not re.search(r'[A-Za-z]', t)


def trunc(s, n=300):
    return s if len(s) <= n else s[:n] + '...'


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--orig', required=True)
    ap.add_argument('--orig-extra', nargs='*', default=[])
    ap.add_argument('--new', required=True)
    ap.add_argument('--min-run', type=int, default=5)
    ap.add_argument('--short-splice', type=int, default=8)
    ap.add_argument('--max-abstract-words', type=int, default=100)
    a = ap.parse_args(argv)

    O = build_orig_tokens(a.orig, a.orig_extra)
    body, blines, regions, line_texts = read_new(a.new)

    # rev statistics (comment-stripped body, top-level marks)
    revs = find_top_revs(body, blines)

    old_text, old_lns = resolve_rev_ln(body, blines, "old")
    N, NL = tokenize_ln(old_text, old_lns)
    covered, segs = match(O, N, a.min_run)

    def is_heading(line):
        return 1 <= line <= len(line_texts) and bool(HEADING_RE.match(line_texts[line - 1]))

    # group uncovered runs, split at heading boundaries
    runs = []
    i = 0
    while i < len(N):
        if covered[i]:
            i += 1
            continue
        h = is_heading(NL[i])
        j = i
        while j < len(N) and not covered[j] and is_heading(NL[j]) == h:
            j += 1
        runs.append((i, j, h))
        i = j

    text_runs, scaf_runs, head_runs = [], [], []
    for (s, e, h) in runs:
        if h:
            head_runs.append((s, e))
        elif all(is_scaffold_token(t) for t in N[s:e]):
            scaf_runs.append((s, e))
        else:
            text_runs.append((s, e))

    ncov = sum(covered)
    pct = 100.0 * ncov / len(N) if N else 100.0
    out = []
    P = out.append

    def fmt_run(s, e):
        l1, l2 = NL[s], NL[e - 1]
        lr = 'line %d' % l1 if l1 == l2 else 'lines %d-%d' % (l1, l2)
        P('  [%s] %s' % (lr, trunc(' '.join(N[s:e]))))
        P('      before: %s' % ' '.join(N[max(0, s - 6):s]))
        P('      after:  %s' % ' '.join(N[e:e + 6]))

    P('== TOKEN COUNTS ==')
    P('original tokens: %d' % len(O))
    P('new tokens (old-resolved): %d' % len(N))
    P('covered tokens: %d (%.2f%%)' % (ncov, pct))
    P('')
    P('== NO-CHECK REGIONS (%d) ==' % len(regions))
    for (s, e, c) in regions:
        P('  lines %d-%d: %d tokens excluded' % (s, e, c))
    P('')
    P('== UNMARKED TEXT RUNS (%d) ==' % len(text_runs))
    for r in text_runs:
        fmt_run(*r)
    P('')
    P('== SCAFFOLD RUNS (%d, informational) ==' % len(scaf_runs))
    for r in scaf_runs:
        fmt_run(*r)
    P('')
    P('== HEADINGS (informational) (%d) ==' % len(head_runs))
    for r in head_runs:
        fmt_run(*r)
    P('')
    shorts = [sg for sg in segs if sg[1] < a.short_splice]
    P('== SHORT SPLICES (< %d tokens, %d, informational) ==' % (a.short_splice, len(shorts)))
    for (s, L, _p) in shorts:
        P('  [line %d] (%d tokens) %s' % (NL[s], L, trunc(' '.join(N[s:s + L]))))
    P('')
    P('== REV STATISTICS (top-level marks in new body) ==')
    P('total marks: %d' % len(revs))
    for tag, c in sorted(Counter(r[1] for r in revs).items()):
        P('  tag %s: %d' % (tag, c))
    P('OLD words total: %d' % sum(len(r[2].split()) for r in revs))
    P('NEW words total: %d' % sum(len(r[3].split()) for r in revs))
    P('10 longest OLD groups:')
    for (ln, tag, old, new) in sorted(revs, key=lambda r: -len(r[2].split()))[:10]:
        P('  line %d, %d words: %s' % (ln, len(old.split()), ' '.join(old.split())[:80]))
    P('')
    new_text, _ = resolve_rev_ln(body, blines, "new")
    aw = abstract_words(new_text)
    abstract_bad = False
    P('== ABSTRACT ==')
    if aw is None:
        P('abstract markers not found')
    elif aw > a.max_abstract_words:
        abstract_bad = True
        P('abstract words: %d (limit %d) TOO LONG' % (aw, a.max_abstract_words))
    else:
        P('abstract words: %d (limit %d) OK' % (aw, a.max_abstract_words))
    P('')
    fail = bool(text_runs) or abstract_bad
    if fail:
        extra = '; abstract too long' if abstract_bad else ''
        P('RESULT: FAIL (%d unmarked text runs%s)' % (len(text_runs), extra))
    else:
        P('RESULT: PASS')
    print('\n'.join(out))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())

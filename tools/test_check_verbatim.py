#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'check_verbatim.py')

S1 = "The quick brown fox jumps over the lazy dog near the quiet river bank."
S2 = "Scheduling vehicles under uncertain demand requires careful planning of every single depot."
S3 = "Passengers board at stops and alight when the trip reaches their final destination."


def doc(body):
    return "\\documentclass{article}\n\\begin{document}\n%s\n\\end{document}\n" % body


class T(unittest.TestCase):
    def run_check(self, orig, new, extra_args=()):
        with tempfile.TemporaryDirectory() as d:
            o = os.path.join(d, 'o.tex')
            n = os.path.join(d, 'n.tex')
            open(o, 'w', encoding='utf-8').write(doc(orig))
            open(n, 'w', encoding='utf-8').write(doc(new))
            p = subprocess.run([sys.executable, SCRIPT, '--orig', o, '--new', n, *extra_args],
                               capture_output=True, text=True)
            return p.returncode, p.stdout

    def test_a_omitted_sentences(self):
        code, out = self.run_check("%s\n%s\n%s" % (S1, S2, S3), "%s\n%s" % (S1, S3))
        self.assertEqual(code, 0, out)
        self.assertIn('RESULT: PASS', out)

    def test_b_changed_word(self):
        new = S1.replace('lazy', 'sleepy')
        code, out = self.run_check(S1 + "\n" + S2, new)
        self.assertEqual(code, 1, out)
        sec = out.split('UNMARKED TEXT RUNS')[1].split('SCAFFOLD RUNS')[0]
        self.assertIn('sleepy', sec)

    def test_c_marked_change(self):
        new = S1.replace('lazy', '\\rev{cc}{lazy}{sleepy}')
        code, out = self.run_check(S1, new)
        self.assertEqual(code, 0, out)

    def test_d_insertion(self):
        new = S1 + " \\rev{cc}{}{A brand new sentence that is not in the original.} " + S2
        code, out = self.run_check(S1 + " " + S2, new)
        self.assertEqual(code, 0, out)

    def test_e_stale_rev_in_original(self):
        orig = "Some leading words here for the context \\rev{zg}{stale old}{current text} and more trailing words follow."
        good = "Some leading words here for the context current text and more trailing words follow."
        bad = "Some leading words here for the context stale old and more trailing words follow."
        code, out = self.run_check(orig, good)
        self.assertEqual(code, 0, out)
        code, out = self.run_check(orig, bad)
        self.assertEqual(code, 1, out)

    def test_f_comment_not_original(self):
        orig = "Visible original sentence is right here today.\n% hidden commented sentence with many many words inside\n"
        code, out = self.run_check(orig, "hidden commented sentence with many many words inside")
        self.assertEqual(code, 1, out)
        # escaped percent is kept
        code, out = self.run_check("Gain of 5\\% over the baseline method is shown here.",
                                   "Gain of 5\\% over the baseline method is shown here.")
        self.assertEqual(code, 0, out)

    def test_g_nested_braces(self):
        orig = "Details are given in Appendix~\\ref{app:x} for all readers of the paper."
        new = "Details are given in \\rev{cc}{Appendix~\\ref{app:x}}{the extended report~\\citep{key}} for all readers of the paper."
        code, out = self.run_check(orig, new)
        self.assertEqual(code, 0, out)
        # does not confuse \review
        code, out = self.run_check(orig, new.replace('\\rev{', '\\review{', 0))
        self.assertEqual(code, 0, out)

    def test_h_nocheck(self):
        new = S1 + "\n%%NOCHECK-BEGIN\nTotally arbitrary text that is nowhere in the source.\n%%NOCHECK-END\n" + S2
        code, out = self.run_check(S1 + " " + S2, new)
        self.assertEqual(code, 0, out)
        self.assertIn('NO-CHECK REGIONS (1)', out)
        self.assertIn('lines 4-6', out)

    def test_i_abstract_too_long(self):
        words = ' '.join('w%d' % i for i in range(120))
        txt = "\\textbf{Abstract}: %s \\textbf{Keywords}: a, b" % words
        code, out = self.run_check(txt, txt)
        self.assertEqual(code, 1, out)
        self.assertIn('TOO LONG', out)
        code, out = self.run_check(txt, txt, ['--max-abstract-words', '200'])
        self.assertEqual(code, 0, out)
        self.assertIn('OK', out)


if __name__ == '__main__':
    unittest.main()

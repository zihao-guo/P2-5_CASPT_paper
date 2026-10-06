# Codex QA record

Independent read-only reviews by Codex (`gpt-6-astra`, reasoning effort `xhigh`), one per modification step.
The files are Codex's answers, unedited.

| Round | Reviewed | Verdict | What was done with the findings |
|---|---|---|---|
| `codex_qa1_plan.md` | Condensation plan and first assembled draft | Plan OK with fixes | All applied in Draft 2 (commit `609148d`), except the OD-connectivity sentence, added in Draft 3. |
| `codex_qa2_draft.md` | Compiled paper (Draft 2): all 36 revision marks, numbers, template | Not ready (2 major, 2 minor) | Both major points fixed in Draft 3 (commit `e5f4b50`). Minor 3 (label inside the authors' Fig. 1) and minor 4 (template prose vs. template code) left to the authors, see below. |
| `codex_qa3_final.md` | Draft 3 and the extended report | Ready with minor fixes | Nested citation parentheses fixed where the layout allowed; extended-report page total fixed. |
| `codex_qa4_verify.md` | The last two fixes | Ready | — |
| `codex_qa5_colour.md` | Extended report: colour description of the Beijing network figures aligned with the figure legend (blue = removed, red = added) | Ready | — |

Open points that are the authors' call:

- Fig. 1 (original image) shows a "Revert to the original" branch, while Rule 1 says the announced network is kept.
- The template's written instructions (24 pt title, upper-case headings, 11 pt captions) differ from what the
  official LaTeX template file actually produces; the paper follows the template file.

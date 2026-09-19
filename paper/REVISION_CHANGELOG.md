# Revision changelog

Baseline: `trace_anomaly_signed_context.pdf` (deposited, 2026-08-03, "second revision",
SHA-256 `3b502dae19986a3d9a4840993f3b5f66988dc0b91ac70e40960d59493970e7e0`, DOI
`10.5281/zenodo.21780964`). This file is untouched; it lives in `~/Downloads` and is not
part of this repository.

Revised: `paper/signed_context_trace_anomaly.tex` / `.pdf` ("third revision"), prepared on branch
`revise-zenodo-signed-context-2026-09`.

No theorem, proof, imported physics equation, non-identifiability claim, or novelty claim in the
baseline is changed. This log distinguishes three kinds of entry:

- **(a)** changes introduced by this revision (additions/sharpenings of the baseline's own content);
- **(b)** inherited baseline bibliographic/metadata problems, found during audit and now corrected;
- **(c)** presentation/reproducibility changes that alter no theorem, proof, or numerical result.

## (a) Changes introduced by this revision

- **Proposition 5.2 (new).** `kappa_cancel = 1 - 1/cond`, `cond = gross/|net|`, identified with the
  classical condition number of a sum. Verified this pass directly against Higham's 1993 paper
  (fetched and read in full): the paper itself states *"the condition number of summation when
  perturbations `x_i -> x_i + Delta x_i` are measured by `max|Delta x_i|/|x_i|`"* for exactly this
  ratio — the citation is primary-source-confirmed, not merely attributed.
- **Remark 5.3 domain correction (this pass).** The first draft of this revision stated
  `cond in [1,infinity]` mapping onto `[0,1]` (closed intervals, attained-value notation). Corrected
  to the mathematically precise statement: for `net != 0`, `cond` is always finite in `[1,infinity)`
  and `kappa in [0,1)`; the value `cond=infinity`/`kappa=1` is never attained by any actual finite
  family with `net != 0`, only approached in the limit of Theorem 6.2(vi). The boundary case
  `net=0, gross>0` is separate — `kappa=1` there directly from Definition 5.1, while `cond` is
  undefined (division by zero), not a literal limit of the `cond` formula. Proposition 5.2's own
  formal statement was already correct and is unchanged.
- **Definition 6.1 footnote restored (this pass).** Re-added the baseline's clarification, dropped
  in the first draft of this revision: *"a group is sign-homogeneous when no two of its nonzero
  terms have strictly opposite signs; adjoining zero terms changes nothing."*
- **Remark 3.2 (new).** `b_a` is the Arnold–Zhai gauge-plus-fermion combination, not the textbook
  one-loop Standard Model beta function (`-41/6`, `19/6`); the two differ by exactly the
  Higgs-doublet term, consistent with Turok–Boyle's emergent-Higgs premise. Verified this pass
  directly against the Turok–Boyle arXiv paper (fetched and read in full): their own text states
  the group data `(C_A, S_F)` for all three factors verbatim, and the "provided the Higgs doublet
  is not a fundamental field" sentence that grounds the emergent-Higgs premise.
- **Remark 5.7 (new).** Explicit numerical witnesses of functional (not merely logical)
  independence of amplitude and tilt on the three-coupling space, correctly scoped as a statement
  about the observation map, not a physical degeneracy. Independently recomputed twice (initial
  revision pass and this audit pass) to full precision.
- **"Contested status" paragraph (Section 2) and Limitation L9 (new).** Notes that Cline & Hell
  (2026, Phys. Rev. D 114, 045022) identify pathologies in the dimension-zero scalar field
  construction the Turok–Boyle mechanism depends on. Verified this pass by retrieving the actual
  published abstract, not merely the DOI metadata: the paper disputes the ghost-free viability of
  the construction across the Boyle–Turok paper series, which grounds (not merely resembles) the
  manuscript's own careful wording ("the construction... depends on", not "the trace-anomaly
  analysis itself").
- **Remark 6.3 and Limitation L8 (new).** Explicit "algebraic witness, not a physical
  decomposition" labeling at every construction used only to prove a mathematical statement.
- **Limitation L7 (new).** Explicit statement that non-identifiability of a decomposition from
  these two observables is not a statement about the physical consistency of the Turok–Boyle
  proposal. Audited this pass specifically for the failure mode of silently strengthening
  "does not uniquely determine an arbitrary decomposition" into "cannot determine the physically
  allowed decomposition" — not found anywhere in the text.

## (b) Inherited baseline problems, found by audit, corrected here

- **Figure 1 restored.** The baseline's two-panel bar chart (level-1 vs. level-2 decomposition,
  referenced by Caution 7.1 and Remark 7.2) was silently omitted from the first draft of this
  revision — a genuine loss not disclosed in the prior changelog. It is restored as a
  self-contained TikZ figure (no `pgfplots` dependency, confirmed unavailable in this TeX
  installation), using exactly the values already verified in Table 3/`tab:levels`: no value was
  invented or altered. Cross-referenced from Remark 7.2. `\usepackage{tikz}` was added to the
  preamble (missing in the first draft, causing a build failure once the figure was added).
- **Appendix A's `0.47, 0.87, 0.98` illustration restored.** This is the baseline's demonstration of
  Theorem 6.2(vi) via an *injected, unrelated canceling pair* `(+X,-X)` adjoined to the three
  level-1 channels — a structurally different construction from Remark 6.4's channel-splitting
  demonstration. Recomputed under the current (unchanged) `net`/`gross`/`kappa` definitions and
  found to reproduce exactly (`0.4723, 0.8707, 0.9849` to 4 places): the illustration was not
  superseded, only accidentally dropped when Appendix A was rewritten to point at the repository.
  Restored as a labelled paragraph, explicitly marked (per L8) as a second algebraic witness.
- **Two self-citation bibliographic errors, inherited from the baseline itself, corrected.**
  Both re-verified directly against the live Zenodo API record for the DOI before correcting:
  - `10.5281/zenodo.20674131`: the baseline's title omitted the subtitle clause
    *", with Two Delimitation Theorems and a Gated Diagnostic Layer"*, present on the live record.
    Restored verbatim.
  - `10.5281/zenodo.20681362`: the baseline cited this DOI under the title *"The Compactness
    Partition on the Period Dial (atlas addendum to 'Compactness as a Thermodynamic Saturation
    Coordinate')"* — but that DOI's live Zenodo record is titled **"Compactness as a Thermodynamic
    Saturation Coordinate: A Conservative Diagnostic Bridge Between Entropic Force, Horizon
    Thermodynamics, and Compact Objects"**, a different title entirely. A search for the
    "atlas addendum" title as cited found no match anywhere. The bibliography entry now uses the
    live record's own title, verbatim, on the same DOI. **This was an error already present in the
    deposited, DOI-bearing baseline (`10.5281/zenodo.21780964`) and in every version before it**;
    it is corrected here but the author should be aware it predates this revision.
- **`@misc` entries did not render their identifiers.** All 6 `@misc` bibliography entries (5
  self-citations plus `TurokBoyle2023`) printed no DOI or URL in the rendered reference list,
  because `plainnat.bst` prints a `url` field but not a `doi` field for that entry type, and none
  of the 5 self-citations had a `url` field populated (only `doi`). All 6 now carry an explicit
  `url = https://doi.org/<DOI>` (or the arXiv abstract URL for Turok–Boyle) and render correctly.

## (c) Presentation / reproducibility changes, no result affected

- **Build recipe corrected.** The documented `pdflatex, bibtex, pdflatex, pdflatex` (3 total
  `pdflatex` passes) sequence does not fully converge this document's table of contents — the "10
  Limitations" and "A Reproducibility" entries print one page early. A 4th `pdflatex` pass is
  required (confirmed: a 5th pass changes nothing further, so 4 is sufficient, not merely
  necessary). **Every build in this revision's history used at least 4 passes**; the previously
  reported PDF hashes were already from converged builds. The recipe is now documented as:
  ```
  pdflatex signed_context_trace_anomaly.tex
  bibtex signed_context_trace_anomaly
  pdflatex signed_context_trace_anomaly.tex
  pdflatex signed_context_trace_anomaly.tex
  pdflatex signed_context_trace_anomaly.tex
  ```
  or, preferably, `latexmk -pdf signed_context_trace_anomaly.tex`, which reruns automatically until
  stable and needs no manually-counted pass sequence.
- Appendix A's pointer to the actual repository and canonical `signedctx.py` (unchanged from the
  first draft of this revision).

## Zenodo metadata warning (not a repository or manuscript change)

**Independently verified via the live Zenodo API**, twice: the version record at
`10.5281/zenodo.21780964` currently carries the metadata title *"Amplitude–Tilt Complementarity and
the Gauge Trace Anomaly as a Signed Context Decomposition..."* — the **first-version** title — while
the PDF actually deposited under that record is titled *"Two Blind Observables on a Signed Gauge
Decomposition..."* This mismatch predates this revision and is not something a GitHub-side change
can fix. **When the next version is deposited, the Zenodo title metadata field must be set
explicitly to the final manuscript title — it will not update automatically from the PDF content.**
See `ZENODO_REVISION_REPORT.md` for the full recommendation.

## Build

`pdflatex` x4 + `bibtex` (see corrected recipe above), TeX Live 2026 (BasicTeX). 0 errors, 0
undefined references/citations, table of contents confirmed converged (5th pass produces
byte-identical text). Page count: 14 (baseline) -> 15 (first draft of this revision) -> **16**
(this corrected revision, reflecting the restored figure and illustration).

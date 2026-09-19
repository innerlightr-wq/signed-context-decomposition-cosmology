# Zenodo Revision Report

Prepared on branch `revise-zenodo-signed-context-2026-09`. Nothing in this report has been
pushed, merged, or uploaded to Zenodo. This report has been updated twice: once after the initial
revision pass, and again after a full adversarial pre-commit audit found several issues, all of
which are now corrected (see "Corrections applied after adversarial audit" below).

## ZENODO METADATA WARNING (read before depositing any new version)

**Independently verified against the live Zenodo API, twice, in two separate audit passes:** the
version record at `10.5281/zenodo.21780964` (which shares concept DOI `10.5281/zenodo.20681973`
with all prior versions — confirming a new version deposit, not a new work, is the correct action)
currently carries the metadata **title** field

> "Amplitude–Tilt Complementarity and the Gauge Trace Anomaly as a Signed Context Decomposition: A
> Partition-Diagnostic Reading of the Turok–Boyle Primordial Spectrum"

— which is the **first-version** title — while the PDF actually deposited under that record is
titled

> "Two Blind Observables on a Signed Gauge Decomposition: An Invariance-Audited Diagnostic Reading
> of the Turok–Boyle Primordial Spectrum"

This mismatch **predates this revision** and cannot be fixed from this repository or by any GitHub
change. **When the next version is deposited on Zenodo, the title metadata field must be set
explicitly to the final manuscript's title — it will not update automatically from the PDF's own
content, and if left as-is (inherited from the prior version) it will continue to mismatch the
deposited file.** This applies regardless of which further revisions are or are not made to the
manuscript text itself.

## Archival baseline

- **File:** `~/Downloads/trace_anomaly_signed_context.pdf` (4 identical copies existed in
  Downloads under numbered-duplicate filenames; all share SHA-256
  `3b502dae19986a3d9a4840993f3b5f66988dc0b91ac70e40960d59493970e7e0`). **Not modified.**
- **Title:** *Two Blind Observables on a Signed Gauge Decomposition: An Invariance-Audited
  Diagnostic Reading of the Turok–Boyle Primordial Spectrum*
- **Author:** Elias De Jesús, Independent Researcher, ORCID 0009-0007-0190-9143
- **DOI:** 10.5281/zenodo.21780964 (per the repository's own README; the live Zenodo record's own
  title metadata does not match — see the warning above)
- **Version/date:** "August 2026 — Technical Note (second revision)"; PDF `CreationDate`
  2026-08-03
- **Page count:** 14. **SHA-256:** as above.
- **Structure:** Abstract; §1 Purpose/scope/non-claims; §2 Turok–Boyle inputs; §3 two-level
  structure (Prop. 3.1, factorization); §4 Reading 1 (Obs. 4.1, two blindnesses); §5 descriptors
  (Def. 5.1, Prop. 5.2 marginal blindness); §6 invariance audit (Thm. 6.2, monotonicity); §7
  alternative decomposition (level 2, gauge/matter, with a two-panel Figure 1); §8 consistency of
  the two readings; §9 epistemic tiers; §10 limitations (L1–L8); §11 conclusion; Appendix A
  reproducibility; 9 references.
- **Principal claims:** the Turok–Boyle amplitude and tilt are each blind, in different ways, to
  the signed channel decomposition of the trace-anomaly coefficient; a cancellation index
  `kappa_cancel` quantifies what is lost; `kappa_cancel` is proved (Thm. 6.2) to be a
  resolution-, scale-, and truncation-dependent descriptor, not an invariant of the physical
  system; `kappa_cancel = 0.20` at the gauge-factor resolution rises to `0.64` under a
  gauge-boson/matter refinement Turok–Boyle display for `SU(3)` and which the note shows holds
  uniformly.
- **Novelty claims:** explicitly conservative already — the note states plainly that the
  blindness proposition is "near-trivial," that the framework contributes "vocabulary... not a
  theorem," and disclaims any new invariant, any validation of Turok–Boyle, and any new cosmology.
- **Limitations/disclaimers:** eight, covering resolution-dependence, truncation-dependence,
  scale-dependence, model-dependence (emergent Higgs), triviality of the core proposition,
  weakness of the complementarity analogy, untestability of an ensemble comparison, and a blanket
  "this note assesses no physics."
- **Computational content:** Tables 3–4's numerical values, Figure 1; an inline, self-contained
  reproducibility script in Appendix A (not tied to any specific repository file).
- **Bibliography:** 9 entries — Turok–Boyle (2023) and 4 self-citations to the author's own prior
  partition-construction series, plus the note's own superseded first version.
- **Reproducibility statement:** present (Appendix A, inline script).
- **AI-assistance disclosure:** present — "AI assistance was used for algebra checking,
  computation, figure generation, manuscript drafting, and adversarial review of two earlier
  drafts. ... All conceptual choices, claims retained, and final responsibility for the work
  belong to the author."

**Assessment of the baseline itself.** This is an unusually careful "second revision": it already
corrects two errors from its own first version (an overstated complementarity claim, and a wrong
sign-cancellation description), already states a four-tier epistemic hierarchy, and already
disclaims Fisher-simplex framing explicitly. The revision work below is therefore incremental,
not a rewrite. **The baseline itself also carries two pre-existing bibliographic errors**,
inherited unchanged through every version up to and including the currently-deposited one — see
"Corrections applied after adversarial audit" below.

## Developments since deposition

Git history: `e5f26f3` (2026-08-03, matches the baseline PDF's creation date) through `cd9d6cc`
(2026-09-18), via two merged pull requests:

- **PR #1**, "Add Zotero literature and provenance audit" — added `docs/NOVELTY_AND_PROVENANCE.md`
  (a claim-by-claim novelty matrix), `docs/LITERATURE_CONTEXT.md` (the physics provenance chain),
  and `references.bib` (22 entries, every one obtained by DOI content negotiation, none from
  memory).
- **PR #2**, "Consolidate canonical Python implementation" — deleted a stale, superseded
  `src/signedctx.py` that the test suite was silently importing instead of the canonical
  root-level `signedctx.py`; removed the `sys.path` manipulation that caused this; added a
  regression guard; documented the fix in `docs/CODE_ARCHITECTURE.md`.

## Research ledger

| # | Item | Deposited baseline says | Repository now establishes | Evidence | Change manuscript? | Category |
|---|---|---|---|---|---|---|
| 1 | `kappa_cancel` identity | Presents `kappa_cancel = 1-|net|/gross` directly, no numerical-analysis framing | `kappa_cancel = 1 - 1/cond`, `cond = gross/|net|` is exactly the classical condition number of a sum (Higham 1993) | Verified directly against Higham's 1993 paper (fetched and read in full: it explicitly names this quantity "the condition number of summation") | **Yes** — new Prop. 5.2 | F, C |
| 2 | Coefficient/coupling provenance | Cites only Turok–Boyle (2023) for both the coefficient formula and the Planck couplings | Coefficient is Arnold–Zhai (1995) Eq. (5.1), quoted by TB; couplings are Buttazzo et al. (2013) via TB's own Ref. [37] | Verified directly against the Turok–Boyle arXiv paper (fetched and read in full): their own text reads "(see Ref. [26], Eq. (5.1))" and "from [37]" at exactly these points | **Yes** — §2 rewritten (TB1/TB2) | F |
| 3 | `b_a` labeling | Calls it "the one-loop β-coefficient combination" unqualified | It is the Arnold–Zhai gauge-plus-fermion combination; differs from the textbook SM one-loop values (`-41/6`, `19/6`) by exactly the Higgs-doublet term | Verified against the Turok–Boyle paper's own stated group data, and arithmetically (`b_Y=-20/3` vs `-41/6`, difference exactly `1/6`; `b_2=10/3` vs `19/6`, difference exactly `1/6`) | **Yes** — new Remark 3.2 | F, C |
| 4 | Turok–Boyle mechanism's contested status | Not mentioned (paper predates the critique) | Cline & Hell (2026, PRD 114, 045022) find pathologies in the dimension-zero scalar construction | DOI and abstract verified; publication date (2026-08-24) confirmed to postdate the baseline deposit (2026-08-03) | **Yes** — new §2 paragraph + Limitation L9 | F |
| 5 | Witness labeling | Distinguishes algebraic constructions from the physical refinement in substance (Remark 7.2) but does not label each construction explicitly | Every witness (two-component split, sign flip, coupling-space variation, injected-pair) explicitly tagged "algebraic witness, not physical" | `docs/NOVELTY_AND_PROVENANCE.md` §6 | **Yes** — new Remark 6.3, Limitation L8 | C |
| 6 | Functional independence of amplitude/tilt | States only logical independence (different functionals) | Explicit numerical witnesses of functional independence on the 3-coupling space | Independently recomputed twice (tilt: `-0.042112 -> -0.046792`; amplitude: `-0.002966` to `-0.003236` at fixed tilt) | **Yes** — new Remark 5.7 | D |
| 7 | Canonical implementation / test suite | Appendix A ships a generic, self-contained inline script (not affected by the bug) | `src/signedctx.py` duplicate deleted; path manipulation removed; 62 tests now exercise the canonical module; guard test added | `docs/CODE_ARCHITECTURE.md`; re-ran `pytest -q` (62 passed) and `python signedctx.py` self-check (all assertions passed) three separate times across this work | **Yes** — Appendix A repointed to the actual repository | G, H |
| 8 | `CITATION.cff` / `paper/README.md` staleness | N/A | Both files named the superseded DOI as "cite this"; now fixed | `docs/NOVELTY_AND_PROVENANCE.md` §9 | No — repository metadata only, not a manuscript claim | H |
| 9 | Ensemble example (`examples/03_structure_and_ensemble.py`) | N/A | Runs an illustrative diagnostic over 4 hypothetical decompositions | Read directly; explicitly self-labeled "certifies nothing... illustrative placeholders" in its own docstring | No new manuscript claim; noted once in Appendix A as explicitly exploratory | I |
| 10 | Figure 1 (level-1/level-2 bar chart) | Present, two-panel bar chart | Was silently dropped in the first draft of this revision (found by audit); restored as a self-contained TikZ figure using Table 3's exact values | Visual inspection of both PDFs; numeric diff confirmed the restored figure introduces only axis-tick numbers, no new data values | **Restored, not new** | C |
| 11 | Appendix A's `0.47/0.87/0.98` illustration | Present (injected-pair construction) | Dropped when Appendix A was rewritten in the first draft (found by audit); recomputed under unchanged definitions, reproduces exactly, restored | Recomputed independently this session: `0.4723, 0.8707, 0.9849` | **Restored, not new** | C |
| 12 | Condition-number interval notation | N/A (new to this revision) | First draft of Remark 5.3 wrote `cond ∈ [1,∞]` into `[0,1]` (closed-interval, attained-value notation) — imprecise, found by audit | Independent edge-case reconstruction (net≠0 vs net=0 vs gross=0) | **Corrected** — half-open intervals, net=0 boundary stated separately | C |
| 13 | Definition 6.1 zero-term footnote | Present in baseline | Dropped in the first draft of this revision (found by audit); restored verbatim as a footnote | Direct baseline-text comparison | **Restored, not new** | C |
| 14 | `DeJesusThalesAtlas2026` / `DeJesusCompactness2026` self-citation titles | As transcribed from baseline reference list | Two discrepancies vs. the live Zenodo record, found by audit; re-verified against the live API before correcting | See "Corrections applied after adversarial audit" | **Corrected, inherited baseline errors** | F |
| 15 | Bibliography DOI/URL visibility | Baseline's own bibliography printed DOIs for all 9 entries | This revision's `@misc` entries (6 of them) printed no identifier at all — a regression, found by audit | Visual inspection of the rendered PDF bibliography before/after | **Corrected** — `url` field added to all 6 `@misc` entries | C |
| 16 | LaTeX build recipe | N/A | The documented 3-pass `pdflatex/bibtex/pdflatex/pdflatex` sequence does not converge this document's TOC; 4 passes needed, found by audit | Direct test: a 3-pass build's TOC differs from a 4-pass build's; a 5th pass changes nothing further | **Documentation corrected**, no manuscript content affected | C |

No item in this ledger is category J (superseded/withdrawn) — nothing established in the baseline
was found to be wrong by this audit; item 3 of the baseline's own text (the sign-cancellation
error, Caution 7.1) was already corrected in the deposited "second revision" itself, prior to this
pass. Items 10–16 were found and fixed during the adversarial pre-commit audit, after the initial
revision pass; see the section below for full detail.

## Corrections applied after adversarial audit

An adversarial pre-commit audit (full text: prior conversation turn) found six issues, none
affecting any theorem, proof, imported physics equation, non-identifiability claim, or novelty
claim. All six are now corrected:

1. **Condition-number interval notation** (Remark 5.3) — corrected to half-open intervals
   `cond∈[1,∞)`, `kappa∈[0,1)` for `net≠0`, with the `net=0` boundary case stated separately as not
   a literal limit of the `cond` formula. Proposition 5.2's own formal statement needed no change.
2. **Sign-homogeneity zero-term clarification** (Definition 6.1) — the baseline's footnote
   ("no two of its nonzero terms have strictly opposite signs; adjoining zero terms changes
   nothing") is restored.
3. **Bibliography DOI/URL visibility** — all 6 `@misc` entries now carry an explicit `url` field
   and render their identifier in the printed bibliography.
4. **Two inherited self-citation title/DOI discrepancies**, re-verified against the live Zenodo
   API before correcting:
   - `10.5281/zenodo.20674131`: restored the omitted subtitle clause, *", with Two Delimitation
     Theorems and a Gated Diagnostic Layer"*.
   - `10.5281/zenodo.20681362`: the baseline cited this DOI as *"The Compactness Partition on the
     Period Dial (atlas addendum to 'Compactness as a Thermodynamic Saturation Coordinate')"*, but
     the DOI's live record is titled **"Compactness as a Thermodynamic Saturation Coordinate: A
     Conservative Diagnostic Bridge Between Entropic Force, Horizon Thermodynamics, and Compact
     Objects"** — a different title. No "atlas addendum" paper matching the old title could be
     located anywhere. The bibliography now uses the live record's own title on the same DOI.
     **This error predates this revision and was present in the currently-deposited baseline
     itself.**
5. **Figure 1 restored** — a self-contained TikZ two-panel bar chart, using exactly the values
   already verified in Table 3, no `pgfplots` dependency (confirmed unavailable in this TeX
   installation). `\usepackage{tikz}` was added to the preamble (a build-breaking omission once
   the figure was added, caught and fixed in the same pass).
6. **Appendix A's `0.47/0.87/0.98` illustration restored** — reproduces exactly
   (`0.4723, 0.8707, 0.9849`) under the unchanged `net`/`gross`/`kappa` definitions, and is
   restored as an explicitly-labeled second algebraic witness alongside Remark 6.4's construction.
7. **Build recipe corrected** — documented as 4 `pdflatex` passes (not 3), or `latexmk -pdf`,
   needed for TOC convergence. Every PDF actually produced and reported in this work's history was
   already built with a converged (≥4-pass) sequence; only the *documented* recipe was
   under-specified.

A systematic numeric diff of the corrected manuscript against the pre-correction revision found
**zero numbers removed** and only the expected additions (Figure 1's axis-tick labels, the
restored `0.4723/0.8707/0.9849` values, and the new DOI-URL numeric prefixes) — confirming no
scientific content was altered by these corrections, only restored or clarified.

## Mathematical corrections

None to the mathematics itself. Every theorem, proof, and identity in the baseline was
independently re-derived across two audit passes (the `b_a`/`P_a` factorization, the
`kappa = 1-1/cond` identity and its exact domain, the `2min(P,N)/(P+N)` form, the level-1/level-2
numbers, the edge cases `net=0 -> kappa=1`, `gross=0 -> kappa=nan`) and found correct. One
presentational imprecision in this revision's own new material (the interval-notation issue in
Remark 5.3, item 12 above) was found and corrected.

## Physics/provenance corrections

Items 2, 3, and 4 of the ledger. None change a physical claim; all sharpen its sourcing, and all
were verified directly against the primary sources (the actual Turok–Boyle and Arnold–Zhai-citing
text, and the Cline–Hell abstract), not merely against secondary repository documentation.

## New results added

Items 1 and 6 of the ledger (the condition-number identity and the functional-independence
witnesses). Both are additions to the diagnostic apparatus around the existing theorems, not new
physics.

## Claims weakened or removed

None removed. One claim is now more precisely scoped than before: the baseline's implicit
treatment of `b_a` as "the" one-loop beta coefficient is now explicitly qualified (Remark 3.2),
without changing any equation.

## Novelty statement, before vs. after

**Before:** "The contribution is a vocabulary in which these distinctions can be stated and
audited, together with the audit itself. It is not new physics, and it is not a result about the
Standard Model."

**After:** Materially the same claim, now anchored to an explicit classical identification:
"`kappa_cancel` is a monotone coordinate on that hierarchy, in exact correspondence with the
classical summation condition number, rather than a property of the system... The contribution is
the systematic application of this classical vocabulary, and the resulting identifiability audit,
to one specific cosmological coefficient whose combination of decomposition-, scale-, and
truncation-dependence had not previously been examined this way." The baseline never overclaimed
`kappa` as a new invariant; the revision makes the reason it is not one explicit and citable
(Higham 1993, primary-source verified) rather than leaving it as an assertion. A full scan of every
occurrence of "new", "invariant", "first", "Fisher", "geometry", "information", "condition",
"diagnostic" and "identifiab-" in the final manuscript found no instance where `kappa` is presented
as a new invariant, and no unscoped priority claim.

## Reproducibility changes

Appendix A no longer presents a free-standing inline script; it names the actual canonical module
(`signedctx.py`), the exact `git clone` / `pip install` / `pytest` commands, and explicitly
separates exact-algebra claims, numerically-checked claims, the restored injected-pair witness, and
the one exploratory example script that contributes no number to the manuscript.

## Files proposed for Zenodo

The existing record (10.5281/zenodo.21780964) currently holds a PDF and a version-suffixed Python
script (`signedctx (5).py`) rather than clean source. Recommended manifest:

- `signed_context_trace_anomaly.pdf` (the rendered note)
- `signed_context_trace_anomaly.tex` (the LaTeX source)
- `references.bib` (the bibliography)

This improves reproducibility over the current deposit without adding repository-internal material
(notes, `docs/`, `tests/`) that does not belong in a scholarly deposit. **Do not re-deposit the
old numbered `signedctx (5).py` file** — the canonical implementation lives in the GitHub
repository and is cited there, not duplicated into the Zenodo record.

## Suggested Zenodo version description

> **Version update (third revision).** This version corrects and sharpens sourcing and exposition
> without changing any theorem, proof, imported physics equation, or numerical value from the
> second revision. Specifically: (1) the trace-anomaly coefficient and its Planck-scale couplings
> are now cited to their true primary sources (Arnold & Zhai 1995; Buttazzo et al. 2013), verified
> directly against the Turok–Boyle paper's own text, not only to Turok & Boyle (2023) themselves;
> (2) the cancellation index `kappa_cancel` is now explicitly identified as a bounded
> reparameterization of the classical condition number of a sum (Higham 1993, verified against the
> primary source), with its exact domain stated precisely; (3) the one-loop combination `b_a` is
> now flagged as the Arnold–Zhai gauge-plus-fermion combination rather than the textbook Standard
> Model one-loop beta function, from which it differs by exactly the Higgs-doublet term; (4) every
> algebraic construction used to witness non-identifiability is now explicitly labeled as such,
> distinct from the one physically motivated refinement in this note; (5) the contested status of
> the underlying Turok–Boyle mechanism in the refereed literature (Cline & Hell 2026) is now noted;
> (6) two inherited bibliographic errors (a mismatched self-citation title/DOI, and a truncated
> subtitle) present since the first version are corrected; (7) the reproducibility appendix now
> points to the accompanying repository's canonical, consolidated implementation. Page count:
> 14 -> 16.

## Remaining concerns

1. Of the cited literature, Higham (1993), Bogachev (2007), Cline & Hell (2026), Arnold–Zhai
   (1995), Buttazzo et al. (2013), Gynther–Vepsäläinen (2006), Machacek–Vaughn (1983), Mihaila et
   al. (2012), and Rothenberg (1971) — all 9 external entries — are now independently verified via
   Crossref and, for the two highest-priority physics sources, by reading the actual cited text
   directly. All 5 self-citation Zenodo DOIs are independently verified via the live Zenodo/
   DataCite API.
2. The **Zenodo title-metadata mismatch on the existing record itself** requires manual correction
   at deposit time — see the warning at the top of this report.
3. Choice of Zenodo file manifest is recommended above (PDF + `.tex` + `.bib`) but not executed.
4. Whether to actually deposit a new Zenodo version is, per instructions, not decided or executed
   here.
5. The figure's panel (b) category labels are legible but sit close to their own bars at 40°
   rotation; a further cosmetic pass (not required) could increase clearance slightly.

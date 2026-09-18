# Novelty and provenance audit

*Zotero-assisted literature, provenance, physics and novelty audit, September 2026. Carried out
after the fact, with the explicit purpose of establishing exactly which parts of this repository
are standard physics, which are imported from Turok–Boyle, which are elementary algebra, and which
— if any — are distinct. Accuracy of physical provenance takes priority over novelty.*

Bibliography: [`../references.bib`](../references.bib) — 22 entries, all with DOIs, every record
obtained from publisher or registry metadata by DOI content negotiation, none typed from memory.

**Headline.** Three things were established, and they should be read together:

1. **The mathematics is classical and now has a precise name.** `gross`/`|net|` is the **condition
   number of a sum** (`Higham1993`), so `kappa = 1 − 1/cond` is a bounded reparameterization of a
   textbook quantity. `net` and `gross` are the total signed mass and total variation mass of the
   Jordan decomposition (`Bogachev2007`), and the whole refinement theorem is the triangle
   inequality. The repository already calls its blindness result "near-trivial as mathematics";
   that assessment extends to the invariance audit as well.
2. **The physics is entirely imported, and the chain is longer than the repository states.** The
   coefficient `c_beta` is Turok–Boyle Eq. (4), which **they quote from Arnold & Zhai (1995),
   Eq. (5.1)**; the Planck-scale couplings come from **Buttazzo et al. (2013)** via their Ref. [37];
   the "95% of the total" figure is **Turok–Boyle's own sentence**; and the `P_3 = 7/6` thermal
   factorization is **theirs for SU(3)**. Neither Arnold–Zhai nor Buttazzo et al. is currently cited.
3. **No prior analysis of this kind was found.** Turok–Boyle's paper has **5 citations and no
   journal version**, and none of the five performs a signed-decomposition, cancellation, or
   observable-blindness analysis of the trace-anomaly coefficient. That makes the *application*
   apparently distinct, while the mathematics behind it is not.

Overall: **the contribution is a diagnostic reinterpretation, resting on classical algebra and
wholly imported physics.** One published critique of the underlying mechanism
(`ClineHell2026`) should be acknowledged.

---

## 1. Claim-by-claim novelty matrix

Classifications: **CLASSICAL** · **STANDARD PHYSICS** · **IMPORTED FROM TUROK–BOYLE** ·
**KNOWN / REPARAMETERIZED** · **ELEMENTARY CONSEQUENCE** · **NEW DERIVATION OF KNOWN INGREDIENTS** ·
**DIAGNOSTIC INTERPRETATION** · **APPARENTLY DISTINCT APPLICATION** · **NUMERICAL ILLUSTRATION** ·
**HEURISTIC** · **UNCERTAIN — MORE SEARCH NEEDED**

| # | Claim / concept | Location | Statement | Closest prior work | Imported? | Convention / approximation | Relationship | Formal status | Classification | Recommended wording | Keys |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `net = Σc_i`, `gross = Σ|c_i|` | README Overview; `net_gross_kappa` | signed total; mobilized magnitude | Jordan/Hahn decomposition: `net = μ(X)`, `gross = |μ|(X)` | no | finite signed measure on a finite set | **identical** | exact | **CLASSICAL** | "the total signed mass and total variation mass of the signed vector read as a discrete signed measure" | `Bogachev2007` |
| 2 | `kappa = 1 − |net|/gross` | README Overview | cancellation index | **`gross/|net|` is the condition number of a sum**; `kappa = 1 − 1/cond`, `cond = 1/(1−kappa)` | no | none | **exact monotone reparameterization, invertible both ways** | exact | **KNOWN / REPARAMETERIZED** | "a bounded reparameterization of the classical condition number of a sum; the only gain over `cond` is boundedness in `[0,1]`" | `Higham1993`, `Higham2002` |
| 3 | `kappa = 2min(P,N)/(P+N)` | README; `sign_masses` | equivalent form | Jordan masses; **formally the Sørensen–Dice form `2min/(sum)`** | no | none | algebraic identity; the Dice resemblance is a **formal analogy only**, different application | exact, verified | **CLASSICAL** (+ analogy) | "an algebraic restatement in terms of the Jordan positive and negative masses" | `Bogachev2007`, `Dice1945` |
| 4 | net invariant under refinement | README Invariance audit | refinement preserves the signed total | finite additivity of a signed measure | no | refinement = children sum to parent | **identical** | exact | **ELEMENTARY CONSEQUENCE** | "finite additivity" | `Bogachev2007` |
| 5 | sign-homogeneous refinement preserves `gross`, `kappa`; sign-crossing strictly increases both; `kappa` monotone non-decreasing | README; `refinement_report` | the monotonicity theorem | `|a+b| ≤ |a|+|b|`, with equality iff same sign; monotonicity of total variation under partition refinement | no | finite sums | **elementary**: the entire theorem is the triangle inequality plus its equality case | exact, verified | **ELEMENTARY CONSEQUENCE** | "an elementary consequence of the triangle inequality and its equality condition; retained as bookkeeping, not offered as a deep theorem" | `Bogachev2007` |
| 6 | any `kappa ∈ [0,1)` realizable at fixed nonzero net | `realize_kappa`; README | two-component construction | immediate algebra | no | `net ≠ 0`; `gross > 0`; two components suffice; `kappa = 1` needs `net = 0` | immediate | exact, verified for 4 targets | **ELEMENTARY CONSEQUENCE** | "immediate algebra; the point is the conclusion it licenses, not the construction" | — |
| 7 | **`kappa` is a resolution-relative coordinate, not an invariant of the physical system** | README | the central conclusion | scheme/decomposition dependence generally | no | — | the sharpest and most useful statement in the repository, and correctly stated | exact | **DIAGNOSTIC INTERPRETATION** | keep as is — this is the repository's best sentence | `Higham1993`, `MachacekVaughn1983` |
| 8 | `c_beta = (125/108)α_Y² − (95/72)α_2² − (49/6)α_3²` | README; `TRACE_ANOMALY` | SM high-T trace anomaly | **Turok–Boyle Eq. (4), quoted by them from Arnold & Zhai (1995) Eq. (5.1)** | **yes, doubly** | high-T, leading perturbative order; Arnold–Zhai's general group formula applied per gauge factor; QED/QCD-derived (full SM pressure: `GyntherVepsalainen2006`) | **identical** | imported | **IMPORTED FROM TUROK–BOYLE** (ultimately **STANDARD PHYSICS**) | "Turok–Boyle Eq. (4), which they take from Arnold & Zhai Eq. (5.1)" — cite Arnold–Zhai directly | `TurokBoyle2023`, `ArnoldZhai1995` |
| 9 | `b_a = (11/3)C_A − (4/3)S_F`; `b_Y = −20/3`, `b_2 = 10/3`, `b_3 = 7` | README Two levels; `beta_coefficient` | the beta combination | **TB state the group data explicitly**: `U(1)_Y: C_A = 0, S_F = ΣY_i² = 5`; `SU(2)_L: C_A = 2, S_F = 3`; `SU(3): C_A = 3, S_F = 3` | **yes** | **these are NOT the textbook SM one-loop beta coefficients**: the standard values are `−41/6` and `19/6`, differing by exactly the `1/6` Higgs-doublet term, absent from the Arnold–Zhai gauge+fermion expression | reproduces TB's own data exactly | verified | **IMPORTED FROM TUROK–BOYLE** | see §4 — the label "one-loop beta-function combination" needs one qualifying clause | `TurokBoyle2023`, `ArnoldZhai1995`, `Mihaila2012` |
| 10 | `c_a = −P_a α_a² b_a`, `P_Y = 25/144`, `P_2 = 19/48`, `P_3 = 7/6` | README; `positive_factors` | factorization | **TB give it for SU(3)**: `T_β = −(12+5n_f)(11−(2/3)n_f)α²T⁴/36`, which at `n_f = 6` is `(7/6)·7` | partly | exact algebra given `b_a`; `P_a` is defined as `−c_a/(α²b_a)` so the identity is automatic | SU(3) row is TB's; the other two are this repository's algebra, as the README already says | exact, verified | **NEW DERIVATION OF KNOWN INGREDIENTS** | the existing wording is correct and now verified against the source | `TurokBoyle2023` |
| 11 | sign pattern `+ − −`; `U(1)_Y` positive because abelian has no gauge self-interaction | README | channel signs | `C_A = 0` for `U(1)` (TB's own table) | yes | signs fixed by `−b_a` since `P_a, α² > 0`; **robust within this expression**, since it needs only `C_A = 0` and `S_F > 0` | correct and now sourced | exact | **STANDARD PHYSICS** | keep; cite TB's group data | `TurokBoyle2023`, `ArnoldZhai1995` |
| 12 | Planck-scale numbers `net = −0.003082`, `gross = 0.003840`, `kappa = 0.1975` | README; `level1` | level-1 values | computed from `α_Y = 0.0181, α_2 = 0.0203, α_3 = 0.0189` — **TB's quoted couplings, from Buttazzo et al. (2013)** | **inputs imported** | SM running at that paper's order/scheme; a specific definition of the Planck scale | arithmetic on imported inputs | verified, reproduces TB's `c_β = −0.0031` | **NUMERICAL ILLUSTRATION** (reproduced from source input) | label "reproduced from source input", never a prediction | `TurokBoyle2023`, `Buttazzo2013` |
| 13 | "the strong channel supplies about 95% of the magnitude of the net" | README | dominance | **TB's own sentence**: "The SU(3) contribution comprises 95% of the total" | **yes** | fraction of net, which is TB's choice of quantity | **imported, not computed here** | verified (`c_3/c_β = 0.947`) | **IMPORTED FROM TUROK–BOYLE** | attribute it to TB; see §6 on whether fraction-of-net is the best quantity | `TurokBoyle2023` |
| 14 | Level 2 gauge/matter split: `gross = 0.008479`, `kappa = 0.6365` | README; `level2` | refinement | splitting `b_a` into `(11/3)C_A` and `−(4/3)S_F` | partly | **legitimate at one loop, where `b_a` is literally that sum**; a diagrammatic grouping, not separately observable; not unique beyond one loop | this repository's refinement of TB's coefficient | exact, verified | **NEW DERIVATION OF KNOWN INGREDIENTS** | "a decomposition of the one-loop coefficient into its antiscreening and screening terms; the pieces are bookkeeping, not separately measurable" | `GrossWilczek1973`, `Caswell1974` |
| 15 | amplitude blindness: `O = f(net)` resolves nothing inside the sum; even `f` also loses the sign | README §1; `decomposition_blindness`, `sign_blindness` | two information losses | **non-identifiability / many-to-one observation map** | no | none | elementary; the README says so | exact, verified | **CLASSICAL** | "standard non-identifiability; the repository's own description of it as near-trivial is right" | `Rothenberg1971` |
| 16 | tilt blindness: `n_s − 1 = −b_3α_3/π` reads only the SU(3) running combination | README §2; `tilt` | one-channel dependence | **TB Eq. (16)**: `n_s ≈ 1 − 7α_3(M_P)/π = 0.958` | **yes** | **TB call this heuristic in their own words** (§4 below) | exact *within TB's approximation*, where the tilt is derived from the SU(3) term alone | verified (`−0.042112` vs TB's `−0.042`) | **IMPORTED FROM TUROK–BOYLE** + **HEURISTIC** | "within Turok–Boyle's heuristic mapping, the tilt depends only on `b_3α_3`" — never "a Standard Model prediction" | `TurokBoyle2023` |
| 17 | the two blindnesses are logically independent | README §1–2 | independence | — | no | — | **true, and stronger than stated**: verified functionally independent on the 3-coupling space (§5) | verified | **DIAGNOSTIC INTERPRETATION** | add the qualification in §5: independent as an observation map, not a degeneracy among realized states | — |
| 18 | scale dependence: `kappa ≈ 0.197` (Planck) vs `≈ 0.002` (electroweak) | README | two orders of magnitude | RG running | inputs partly imported | **Planck row uses TB/Buttazzo couplings; the electroweak row is constructed here** from `α_em = 1/128`, `sin²θ_W = 0.231`, with the high-T expression applied outside its regime | the existing "illustrative only" caveat is appropriate and sufficient | verified | **NUMERICAL ILLUSTRATION** | keep the caveat; state explicitly that the electroweak couplings are not from a cited source | `Buttazzo2013` |
| 19 | perturbative-order dependence via mixed-coupling terms | README | order dependence | **two-loop gauge beta functions contain gauge-mixing, Yukawa and scalar terms** | no | — | **the literature confirms the repository's claim.** Beyond one loop the beta functions are not a sum of per-factor terms, so the channel list is not closed and mixed terms need a convention | correct | **STANDARD PHYSICS** (supporting the repo's claim) | cite Machacek–Vaughn / Mihaila et al.; note this *complicates* rather than *invalidates* the leading-order decomposition | `MachacekVaughn1983`, `Mihaila2012`, `Caswell1974` |
| 20 | signed L¹ is not a Fisher simplex | README | rejection of simplex geometry | signed-measure total variation is the right framework | no | — | **correct, and the audit confirms the better framework is Jordan decomposition / total variation, not any signed-simplex geometry** | exact | **CLASSICAL** | keep; name total variation as the framework that does apply | `Bogachev2007` |
| 21 | the whole diagnostic applied to TB's gauge decomposition | the repository as a whole | — | **none found**: TB has 5 citations, no journal version, and none of the five does this | no | — | see §7 | — | **APPARENTLY DISTINCT APPLICATION** | "No prior decomposition-level analysis of this coefficient was identified in the literature reviewed" — no priority claim | `TurokBoyle2023`, `ClineHell2026`, `BarvinskyWachowski2023`, `Quintin2024` |

## 2. `PHYSICS INPUT → REPOSITORY USE`

| Input | Source | Physical status | Approximation / order | Scale / scheme | Used in | Does the repo independently establish it? |
|---|---|---|---|---|---|---|
| `c_beta` coefficient `(125/108, −95/72, −49/6)` | `ArnoldZhai1995` Eq. (5.1), **via** `TurokBoyle2023` Eq. (4) | established thermal field theory | leading perturbative contribution to `T_β`; three-loop free-energy paper | high temperature; QED/QCD general group formula applied per SM factor | `TRACE_ANOMALY`, `level1`, `level2` | **No** |
| Group data `C_A, S_F` per factor (`S_F = ΣY_i² = 5` for `U(1)_Y`) | `TurokBoyle2023`, explicit in their text | standard group theory | one loop | — | `beta_coefficient` | **No** |
| Planck-scale couplings `0.0181, 0.0203, 0.0189` | `Buttazzo2013`, **via** `TurokBoyle2023` Ref. [37] | standard SM running | state-of-the-art RG at that paper's order | Planck scale, MS-bar-type | `level1`, `level2`, `tilt` | **No** |
| Amplitude relation `P_R ∝ c_beta²` | `TurokBoyle2023` | **proposal-internal** | leading order in their framework | — | README §1 | **No** |
| Tilt relation `n_s − 1 = −b_3α_3/π` | `TurokBoyle2023` Eq. (16) | **explicitly heuristic, by their own statement** | heuristic wavelength↔RG-scale mapping | Planck scale | `tilt` | **No** |
| "SU(3) is 95% of the total" | `TurokBoyle2023` | their own arithmetic | — | Planck scale | README | **No** (reproduced) |
| `P_3 = 7/6` thermal reading | `TurokBoyle2023` (SU(3) only) | their interpretation | `n_f = 6` | high-T | `positive_factors` | **No** for SU(3); the other two rows are this repo's algebra |
| Observed `n_s = 0.9587 ± 0.0056` | `Planck2018X` | **observation** | — | — | README/validate comparison | **No** |
| Electroweak `α_em = 1/128`, `sin²θ_W = 0.231` | **not cited** — constructed in `signedctx.py` | textbook values | — | electroweak | `level1("electroweak")` | constructed here; label as illustrative |
| Higher-order mixed terms | `MachacekVaughn1983`, `Mihaila2012` | established | two/three loop | scheme-dependent | README order-dependence claim | **No** (cited as support) |

**Nothing in the physics column is established by this repository.** Every number it prints is a
function of imported inputs. The repository's own content is the algebra applied to them.

## 3. `WHAT CHANGES UNDER WHAT?`

| Operation | `net` | `gross` | `kappa` | amplitude `∝ net²` | tilt `−b_3α_3/π` | physical interpretation |
|---|---|---|---|---|---|---|
| channel relabeling | — | — | — | — | — | none; pure bookkeeping |
| sign-homogeneous refinement | — | — | — | — | — | none; finer labels, same content |
| sign-crossing refinement | — | **increases** | **increases** | — | — | reveals sign structure the coarser labelling hid |
| opposite-sign merging | — | **decreases** | **decreases** | — | — | hides sign structure |
| global sign flip `c_i → −c_i` | flips | — | — | — | — | not a physical operation on the SM coefficient |
| RG-scale change | changes | changes | **changes** (0.197 → 0.002) | changes | changes | **physical**: couplings run |
| perturbative-order change | changes | changes | **changes** | changes | changes | **scheme/convention entangled**: mixed terms need an assignment convention |
| basis/channel convention change | — | may change | **may change** | — | — | resolution choice, not a property of the system |

Read down the `kappa` column: it is invariant under exactly the operations that carry no
information (relabeling, sign-homogeneous refinement, global sign flip) and varies under
everything else — including two operations (scale, order) that are *physical or conventional*
rather than merely bookkeeping. That is the precise content of "not an invariant of the
underlying physical system".

## 4. The one wording qualification the physics requires

README's Level-2 table calls `b_a = (11/3)C_A − (4/3)S_F` the "one-loop beta-function
combination". **The values are correct** — they reproduce TB's own quoted `(C_A, S_F)` data
exactly, and were verified here: `b_Y = −(4/3)(5) = −20/3`, `b_2 = 22/3 − 4 = 10/3`,
`b_3 = 11 − 4 = 7`.

But they are **not the textbook SM one-loop gauge beta coefficients**, which are `−41/6` and
`19/6` in SM hypercharge normalization. Each differs by exactly `1/6` — the contribution of a
**fundamental Higgs doublet**, which is absent from the Arnold–Zhai gauge-plus-fermion
high-temperature expression.

Two points, and the second matters:

* the README should say *which* combination it means, since a reader who checks against a
  textbook will find a mismatch;
* the omission is **consistent with Turok–Boyle's own premise**, since their mechanism requires
  the Higgs doublet to be **emergent rather than fundamental** ("provided the Higgs doublet is not
  a fundamental field"). So this is a coherence point in TB's favour, not an error.

Recommended clause: *"`b_a` here is the Arnold–Zhai gauge-plus-fermion combination as quoted by
Turok–Boyle; it coincides with the one-loop beta coefficient only when no fundamental scalar
contributes, which is consistent with the emergent-Higgs premise of their framework and differs
from the textbook SM values `−41/6`, `19/6` by exactly the Higgs-doublet term."*

**No equation or numerical value should change.** Per the audit brief this is reported, not
silently reconciled.

## 5. Are the two blindnesses physically independent?

**Logically independent: yes, and verifiably so.** Treating `(α_Y, α_2, α_3)` as free, the audit
constructed both witnesses numerically:

* **same amplitude, different tilt** — holding `c_beta = −0.003082` fixed and moving `α_3` from
  `0.0189` to `0.0210` (with `α_Y` solved to compensate) moves `n_s − 1` from `−0.042112` to
  `−0.046792`;
* **same tilt, different amplitude** — holding `α_3` fixed and moving `α_2` over `0.018–0.023`
  moves `c_beta` over `−0.002966` to `−0.003236` with the tilt unchanged.

So the two observables are genuinely functionally independent on the three-coupling space, not
merely independent as abstract functionals. (Note the family is constrained: at `α_3 = 0.017`
there is no real `α_Y` holding `c_beta` fixed.)

**Physically independent: not established, and the repository should not imply it.** At the SM
Planck point the three couplings are *determined*, not free. The witnesses above therefore
describe the **observation map of the model family**, not a degeneracy among physically realized
states. This is a sensitivity/identifiability statement about the proposal, which is the useful
reading, and it is weaker than a claim about nature.

## 6. Physical realizability of each witness — the labels step 19 asks for

| Witness | What it is |
|---|---|
| `level1` → `level2` (gauge factors → gauge/matter) | **a legitimate refinement of the same physical expression** at fixed order and scale |
| `decomposition_blindness`: resolved 3-channel vs single channel with equal net | **algebraic witness only** — a single-channel "context" is not a physical SM decomposition |
| `realize_kappa(net, target)` for `kappa ∈ {0, 0.25, 0.5, 0.9}` | **arbitrary two-component signed vectors** — pure algebra, no physical content |
| `sign_blindness`: `c_i → −c_i` | **algebraic witness only** — the global sign of the SM trace-anomaly coefficient is not a free parameter |
| Theorem 6.2(vi) refinement `c_r → (c_r + X, −X)` for `X` up to `1000` | **algebraic witness**, deliberately far outside physical magnitudes |
| Planck vs electroweak `kappa` | **a genuine physical change** (running couplings), though the electroweak row applies the high-`T` expression outside its regime |
| the `(α_Y, α_2, α_3)` variations of §5 | **model-family variation**, not realized SM states |

The repository's existing text does not confuse these, but it does not label them either. Adding
the labels is the single most useful documentation change after the citations.

## 7. Has anyone done this before?

**Not found.** `TurokBoyle2023` has **5 citations** (OpenAlex, September 2026) and **no located
journal version** — it remains a February 2023 arXiv preprint. The five citing works are:

| citing work | what it does | does it do this analysis? |
|---|---|---|
| `ClineHell2026`, *Pathologies of dimension-zero scalar fields*, PRD **114**, 045022 | **refereed critique** of the `(□φ)²` scalars and of the claim that their fluctuations source the primordial perturbations | no — it attacks the mechanism, not the decomposition |
| `BarvinskyWachowski2023`, PRD **108**, 045014 | conformal anomaly, nonlocal effective action, running scale | no |
| `Quintin2024`, JCAP **09**, 026 | fingerprints of a non-inflationary universe from massive fields | no |
| `MillerVolovikZubkov2022` (related line) | zero-dimension scalar from anomaly cancellation | no |
| Kahan (2024, ×2) | quantum-cosmology essays | no |

So: **no prior analysis of the Turok–Boyle trace-anomaly coefficient in terms of positive/negative
channel cancellation, gross versus net, decomposition depth, or observable blindness was
identified in the literature reviewed.** That is the correct wording — an absence in a
five-paper citation network is weak evidence, and no priority should be claimed.

**One thing the repository should add.** `ClineHell2026` is a refereed paper finding pathologies in
the very ingredient the analysed mechanism depends on. The repository is right to take no position
on the mechanism, but a reader deserves to know the proposal is **contested in the refereed
literature**, not merely unverified by its own authors. One sentence suffices.

## 8. Claim-strength audit

Searched across `README.md`, `CITATION.cff`, `paper/README.md`.

| phrase | count | verdict |
|---|---|---|
| "new" | 1 | **SAFE** — inside a non-claim ("does not … establish a **new** cosmological model") |
| "universal" | 1 | **SAFE** — "Neither value of `kappa` is **universally** 'the correct one'" |
| "Standard Model constant" | 1 | **SAFE** — inside a non-claim |
| "invariant" / "invariance" | 3 (+code keys) | **SAFE** — every occurrence is scoped: "not an **invariant** of the underlying physical system", "**invariant** under a global sign flip", "**invariance** under relabeling / under sign-homogeneous refinement". No unqualified use, and no RG-, gauge- or scheme-invariance is claimed anywhere |
| "exact" | 5 | **SAFE** — technical ("exact cancellation", "Exact algebra") |
| "independent" | 3 | **NEEDS QUALIFICATION** (one instance) — "the two blindnesses are logically independent" is true as written, but should note that logical independence is not physical independence; see §5 |
| "novel", "discovered", "first", "fundamental", "prediction", "explains", "determines", "derives", "robust", "scale-independent", "model-independent" | 0 | — |

**The claim strength is already well calibrated** — notably, zero uses of "prediction", "explains"
or "derives", and the word "invariant" is scoped everywhere it appears. The audit recommends no
downgrades, only the one qualification above plus the citations.

## 9. Repository-integrity findings (not provenance)

Found while reading, and reported because they affect what a reader is actually running:

1. **Two different implementations were shipped — FIXED.** Root `signedctx.py` (587 lines)
   implements the current manuscript; `src/signedctx.py` (523 lines) implemented the **superseded**
   manuscript and lacked the entire invariance-audit API. A function-by-function comparison found
   every `src`-only name to be a rename of a canonical function, no functionality unique to `src/`,
   and **no mathematical disagreement** — `net_gross_kappa` agreed exactly, including the
   `gross = 0 → nan` edge case. `src/signedctx.py` has been deleted.
2. **The test suite exercised the stale copy — FIXED.** `tests/conftest.py` and all three
   `examples/` inserted `src/` on `sys.path`, so `import signedctx` resolved to the stale file under
   pytest and to the canonical file interactively. The 44 passing tests never touched `level1`,
   `level2`, `refine`, `realize_kappa` or `tilt`. The path manipulation is gone, the suite now
   imports the canonical module (62 tests), and a guard test fails if a duplicate ever shadows it
   again. See [`CODE_ARCHITECTURE.md`](CODE_ARCHITECTURE.md).
3. **`paper/README.md` contradicted `README.md` — FIXED in this audit.** It named the superseded
   DOI `10.5281/zenodo.20701311` as "cite this", gave a different concept DOI
   `10.5281/zenodo.20681973`, and used the old title. It now points at
   `10.5281/zenodo.21780964`, labels the earlier version as superseded, and records the
   physics-provenance chain.
4. **README "Repository organization" omitted `src/`, `examples/`, `requirements.txt` and
   `tests/conftest.py` — FIXED**, together with a note distinguishing the two implementations.

All four items are now addressed. Items 1 and 2 were resolved by a separate code-consolidation
change, which altered no equation and no numerical value: the self-check output of
`python signedctx.py` is byte-identical before and after.

## 10. Unresolved questions

1. Whether an exact prior use of `1 − |Σc|/Σ|c|` as a *named* index exists in a field not
   searched here. The condition-number identification (§1 row 2) is exact and is the right
   citation regardless.
2. Whether `2min(P,N)/(P+N)` has been used as a cancellation measure under the Sørensen–Dice
   name; the formal coincidence is noted, the application is different. Tagged
   `uncertain-more-search`.
3. Whether the level-2 gauge/matter split has an accepted interpretation as anything more than
   diagrammatic bookkeeping. The audit found no support for treating the pieces as separately
   observable, and the repository does not claim they are.

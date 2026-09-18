# Signed Context Decomposition

Reference implementation accompanying the technical note

> **Two Blind Observables on a Signed Gauge Decomposition: An Invariance-Audited Diagnostic Reading of the Turok–Boyle Primordial Spectrum**
> Elias De Jesús (2026)

- Manuscript revision accompanying this repository: <https://doi.org/10.5281/zenodo.21780964>
- Earlier manuscript version, now superseded: <https://doi.org/10.5281/zenodo.20701311>

This is a scientific software repository, not a software product. It exists so that the
computational content of the note can be inspected, checked, and rerun.

The module evaluates signed decompositions, tests the invariance properties of their summary
quantities, and demonstrates the algebraic blindness of observables that depend only on a
signed net.

---

## Overview

A *signed context* is a finite vector of signed channel contributions `c_i`. The module
computes three descriptors:

| Quantity | Definition | Meaning |
| --- | --- | --- |
| `net` | `Σ cᵢ` | the signed total |
| `gross` | `Σ abs(cᵢ)` | the total mobilized magnitude |
| `kappa` | `1 − abs(net) / gross` | the cancellation index |

Writing `P` for the sum of the positive contributions and `N` for the absolute sum of the
negative ones, the cancellation index also satisfies

```
kappa = 2 · min(P, N) / (P + N)
```

Both forms are checked against each other by the validation routine.

> **What `kappa` already is.** Reading `c` as a discrete signed measure, `net` is its total signed
> mass and `gross` its total variation mass (Jordan decomposition). And `gross/abs(net)` is the
> classical **condition number of a sum** — the factor in the standard error bound for
> floating-point summation — so
>
> ```
> cond = gross/abs(net) = 1/(1 − kappa)        kappa = 1 − 1/cond
> ```
>
> Both directions are exact: `kappa` is a **bounded reparameterization of a textbook quantity**,
> not a new index, and its only advantage over `cond` is that it lies in `[0,1]`. See
> [`docs/LITERATURE_CONTEXT.md`](docs/LITERATURE_CONTEXT.md) §3.

Interpretation:

- `kappa = 0` — all nonzero channels have the same sign.
- `0 < kappa < 1` — partial cancellation.
- `kappa = 1` — exact cancellation, `net = 0`, provided `gross > 0`.
- `kappa` is undefined (returned as `nan`) when `gross = 0`.

A central conclusion of the revised manuscript is that **`kappa` is not a decomposition-free
property of a physical system.** It is a descriptor of a specified decomposition at a
specified renormalization scale and perturbative truncation.

---

## Scientific motivation

Turok and Boyle use the high-temperature Standard Model trace-anomaly coefficient — their Eq. (4),
which **they in turn quote from Arnold & Zhai (1995), Eq. (5.1)**, with the Planck-scale couplings
taken from Buttazzo et al. (2013) via their Ref. [37]. Every number below is a function of those
imported inputs; see [`docs/NOVELTY_AND_PROVENANCE.md`](docs/NOVELTY_AND_PROVENANCE.md) §2 for the
full input table.

```
c_beta = (125/108)·α_Y²  −  (95/72)·α_2²  −  (49/6)·α_3²
```

in their proposed account of the primordial scalar spectrum. At the Planck-scale couplings
quoted in their work, the three gauge-factor contributions have the sign pattern

| Channel | Sign |
| --- | --- |
| `U(1)_Y` | positive |
| `SU(2)_L` | negative |
| `SU(3)_c` | negative |

The weak and strong contributions therefore have the **same** sign. Only the hypercharge
contribution is positive, and by `kappa = 2·min(P, N)/(P + N)` the cancellation index at this
resolution is carried entirely by that single positive channel.

At the gauge-factor resolution the values are

```
net   = −0.003082
gross =  0.003840
kappa =  0.1975
```

The strong channel supplies about 95% of the magnitude of the net — this is **Turok and Boyle's own
figure** ("The SU(3) contribution comprises 95% of the total"), reproduced here, not computed
independently.

The note studies two different forms of observable blindness.

### 1. Amplitude blindness

The scalar amplitude is proportional to the square of the trace-anomaly coefficient,
`P_R ∝ c_beta²`. Being an *even* function of the net, it reads only the **magnitude** of the
net signed sum. It is blind to:

- the internal channel decomposition;
- the gross magnitude;
- the cancellation index;
- the overall sign of `c_beta`.

Two decompositions with equal net produce the same amplitude, regardless of how much
sign-opposed structure lies underneath. The two blindnesses are logically independent: an
*odd* observable would resolve the sign while remaining blind to the decomposition, which
`sign_blindness(context, power=1)` demonstrates.

Amplitude and tilt are also **functionally** independent on the three-coupling space: holding
`c_beta` fixed while moving `α_3` changes the tilt, and holding `α_3` fixed while moving `α_2`
changes the amplitude. That is a statement about the **observation map of the model family**, not a
degeneracy among physically realized states — at the Standard Model Planck point the three
couplings are determined, not free.

### 2. Tilt blindness

Under the heuristic wavelength-to-running assumptions used by Turok and Boyle, the spectral
tilt reads the dominant `SU(3)` running combination `b₃·α₃` rather than the full
three-channel coefficient. It is therefore insensitive to:

- the positive prefactor multiplying the dominant channel;
- the `U(1)_Y` channel;
- the `SU(2)_L` channel;
- the complete signed decomposition.

The amplitude and tilt are thus **not** complementary partition coordinates. They are better
described as two different projections of a nested, two-level structure.

---

## Two decomposition levels

The gauge-factor contributions can be written algebraically as

```
c_a = −P_a · α_a² · b_a          with  P_a > 0
b_a = (11/3)·C_A − (4/3)·S_F     (one-loop beta-function combination)
```

The positive factors and beta combinations are

| Channel | `P_a` | `b_a` |
| --- | --- | --- |
| `U(1)_Y` | 25/144 | −20/3 |
| `SU(2)_L` | 19/48 | 10/3 |
| `SU(3)_c` | 7/6 | 7 |

> **Convention.** These `b_a` follow from the group data Turok and Boyle state explicitly
> (`U(1)_Y`: `C_A = 0`, `S_F = Σ Y_i² = 5`; `SU(2)_L`: `C_A = 2`, `S_F = 3`; `SU(3)_c`: `C_A = 3`,
> `S_F = 3`). They are the **Arnold–Zhai gauge-plus-fermion combination**, which coincides with the
> one-loop beta coefficient only when no *fundamental* scalar contributes: the textbook Standard
> Model values are `−41/6` and `19/6`, differing by exactly the `1/6` Higgs-doublet term. That
> omission is consistent with Turok and Boyle's premise that the Higgs doublet is emergent rather
> than fundamental. No equation or value here is changed by this observation; it is recorded so a
> reader checking against a textbook is not misled.

Because `P_a` and `α_a²` are positive, the sign of each gauge-factor contribution is carried
by `−b_a`. The `U(1)_Y` term is positive because an abelian factor has no gauge
self-interaction contribution, leaving only the matter-screening part; the two non-abelian
terms are negative because gauge-boson antiscreening dominates.

Note that the `α²` cancels in `P_a = −c_a / (α_a²·b_a)`, so each `P_a` is a pure rational
number and does not run. Turok and Boyle supply a *thermal* interpretation of this factor for
`SU(3)` only; for the other two channels the factorization implemented here is algebraic, and
no thermal identification is claimed.

**Level 1 — gauge factors** (`U(1)_Y`, `SU(2)_L`, `SU(3)_c`) at the Planck scale:

```
net   ≈ −0.003082
gross ≈  0.003840
kappa ≈  0.1975
```

**Level 2 — gauge-boson and matter pieces.** Resolving each beta combination into its
antiscreening and screening parts gives `U(1)_Y matter`, `SU(2)_L gauge`, `SU(2)_L matter`,
`SU(3)_c gauge`, `SU(3)_c matter`:

```
net   ≈ −0.003082   (unchanged)
gross ≈  0.008479
kappa ≈  0.6365
```

Neither value of `kappa` is universally "the correct one." Each describes a stated
resolution.

---

## Invariance audit

The manuscript proves the following refinement properties, and the module checks them.
A *refinement* splits a contribution into pieces **assigned to it** whose sum equals it;
adjoining an unassigned `(+X, −X)` pair is not a refinement and `refine()` rejects it.

**Preserved under every refinement.** The signed net is unchanged.

**Sign-homogeneous refinement** — every child shares its parent's sign (zeros ignored):

```
gross_refined = gross_original
kappa_refined = kappa_original
```

Examples: relabeling channels; splitting a positive channel into positive pieces; splitting a
negative channel into negative pieces; merging channels of the same sign.

**Sign-crossing refinement** — a channel split into pieces of opposite sign:

```
gross_refined > gross_original
kappa_refined > kappa_original
```

Consequently `kappa` is monotone non-decreasing under refinement. Merging opposite-sign
channels has the reverse effect and decreases it.

These are **elementary**: net-invariance is finite additivity, and the gross statement is
`abs(a+b) ≤ abs(a) + abs(b)` together with its equality case. They are retained as explicit
bookkeeping, not offered as deep results.

**No decomposition-free value.** For a fixed nonzero net, decompositions exist with `kappa`
arbitrarily close to 1; coarsening the whole vector to a single channel gives `kappa = 0`.
`realize_kappa(net, target)` constructs a two-component decomposition hitting any target in
`[0, 1)` at fixed net. **These constructions are algebraic witnesses, not physical states:** an
arbitrary two-component signed vector, a single-channel context, and a global sign flip are none of
them physically realizable Standard Model decompositions. The one genuinely physical comparison in
this repository is level 1 versus level 2 (a legitimate refinement of the same expression at fixed
order and scale) and the change of renormalization scale. The labels for every witness are
tabulated in [`docs/NOVELTY_AND_PROVENANCE.md`](docs/NOVELTY_AND_PROVENANCE.md) §6. Therefore:

> `kappa` is a resolution-relative coordinate, not an invariant of the underlying physical
> system.

`kappa` is also invariant under a global sign flip `cᵢ → −cᵢ`, so the descriptors recover what
the amplitude loses about the decomposition but not what it loses about the sign.

---

## Scale and truncation dependence

The channel values depend on the renormalization scale through the running couplings. Using
the same leading expression:

| Scale | Approximate `kappa` |
| --- | --- |
| Planck | 0.197 |
| Electroweak | 0.002 |

The electroweak row is illustrative only: it applies the same high-temperature expression at a
scale where its physical applicability and perturbative hierarchy both differ. The two orders
of magnitude are the point; the second digit is not.

The decomposition is also tied to perturbative order. At higher orders, mixed-coupling terms
can involve more than one gauge factor, requiring either additional interaction channels or an
explicit convention assigning them to existing ones. Either route is itself a resolution
choice, and by the monotonicity result it moves `kappa`. The channel list is therefore part of
the stated analytical resolution.

---

## What is exact, interpretive, and not claimed

**Exact algebra.** The module evaluates or checks: `net`; `gross`; `kappa`; the equivalent
positive/negative-mass form; invariance under relabeling; invariance under sign-homogeneous
refinement; monotonicity under sign-crossing refinement; decomposition blindness of observables
`O = f(net)`; additional sign blindness when `f` is even; and the level-1 and level-2 numerical
decompositions.

**Imported physical statements.** The amplitude relation and the proposed tilt relation belong
to the Turok–Boyle framework. Their tilt analysis is explicitly heuristic and depends on
assumptions connecting spatial wavelength to renormalization-group running, which the authors
state they have not verified. This repository does not strengthen the epistemic status of that
argument.

For completeness: the Turok–Boyle paper is an arXiv preprint with no journal version located, and
its central ingredient — dimension-zero scalar fields — has since been criticized in the refereed
literature (J. M. Cline and A. Hell, *Pathologies of dimension-zero scalar fields*,
Phys. Rev. D **114**, 045022, 2026). **This repository takes no position either way**; the
diagnostic below is about what the observables can resolve, not about whether the mechanism is
correct.

**Structural interpretation.** Diagnostic readings rather than physical results: amplitude and
tilt as two different blindnesses; `kappa` as a resolution-depth coordinate; the
level-1-to-level-2 change in `kappa` as a measure of sign structure hidden by a coarser
labeling.

**Non-claims.** This repository does not validate the Turok–Boyle construction; derive the
primordial spectrum; extend or critique their physical mechanism; establish a new cosmological
model; treat `kappa ≈ 0.20` as a Standard Model constant; attach significance to its numerical
proximity to 1/5; or identify a mixed-sign vector with a Fisher probability simplex.

---

## Signed L¹ structure is not a Fisher simplex

The gauge contributions have mixed signs and therefore do not form a probability simplex. The
context-resolver framework for positive components assumes `cᵢ ≥ 0` and uses Fisher information
geometry on a normalized positive composition; those assumptions do not hold here.

The blindness statement implemented here is purely algebraic: *an observable that depends only
on the sum cannot resolve the terms inside that sum.* It is near-trivial as mathematics, and
its interest lies in what it licenses one to ask, not in the statement itself.

Normalizing the absolute values would create a positive simplex, but would discard the sign
information that motivates the analysis. `classify_structure()` distinguishes mixed-sign
structures from positive simplex-like inputs and refuses to apply Fisher-geometric
interpretations to signed data.

---

## Relation to prior work

A provenance audit (September 2026) is recorded in
[`docs/NOVELTY_AND_PROVENANCE.md`](docs/NOVELTY_AND_PROVENANCE.md) and
[`docs/LITERATURE_CONTEXT.md`](docs/LITERATURE_CONTEXT.md), with verified records in
[`references.bib`](references.bib). In summary:

| part | status |
|---|---|
| `net`, `gross` | total signed mass and total variation mass of a Jordan decomposition — **classical** |
| `kappa` | bounded reparameterization of the **condition number of a sum** — **known / reparameterized** |
| refinement monotonicity | the **triangle inequality** and its equality case — **elementary** |
| amplitude blindness | standard **non-identifiability** of a many-to-one observation map — **classical** |
| `c_beta`, the couplings, the amplitude and tilt relations, the 95% figure | **imported** from Turok–Boyle, and behind them Arnold–Zhai and Buttazzo et al. |
| the gauge/matter level-2 split | this repository's refinement of the one-loop coefficient; legitimate at that order, diagrammatic bookkeeping rather than separately observable |
| the combined diagnostic applied to this coefficient | **no equivalent analysis was identified in the literature reviewed** (Turok–Boyle has five citations and none performs one); no priority is claimed |

So the mathematics is classical, the physics is wholly imported, and what the repository
contributes is the **diagnostic reading**: a systematic account of what these two observables can
and cannot resolve about the decomposition beneath them.

## Repository organization

```
README.md
LICENSE
CITATION.cff
requirements.txt
references.bib            verified bibliography for the provenance audit
docs/
    NOVELTY_AND_PROVENANCE.md   claim-by-claim matrix, physics-input and invariance tables
    LITERATURE_CONTEXT.md       provenance chain and the classical mathematics
signedctx.py              current implementation (accompanies the current manuscript)
src/signedctx.py          EARLIER implementation, kept for the superseded manuscript
examples/                 three runnable demonstrations (import from src/)
tests/
    conftest.py
    test_signedctx.py     exercises src/signedctx.py
```

> **Note on the two implementations.** The root `signedctx.py` is the version accompanying the
> current manuscript and provides the invariance-audit API (`level1`, `level2`, `refine`,
> `refinement_report`, `realize_kappa`, `sign_blindness`, `tilt`). `src/signedctx.py` is the
> earlier implementation for the superseded manuscript and does not provide those functions.
> `pytest tests` and the `examples/` scripts currently import from `src/`; the current
> implementation is checked by its own `python signedctx.py --validate` self-check.

The manuscript is archived on Zenodo rather than committed as an authoritative publication
file.

---

## Installation

Python 3.9 or newer and NumPy are required.

```bash
git clone https://github.com/innerlightr-wq/signed-context-decomposition-cosmology.git
cd signed-context-decomposition-cosmology
pip install -r requirements.txt
```

No packaging step is required.

---

## Basic usage

```python
from signedctx import analyze

context = analyze(
    ["U(1)_Y", "SU(2)_L", "SU(3)_c"],
    [+0.0003792, -0.0005437, -0.0029170],
)

context.net       # -0.0030815
context.gross     #  0.0038399
context.kappa     #  0.19750
context.dom_ch    # 'SU(3)_c'
print(context.summary())
```

The hand-typed values above are rounded; `level1()` computes the channels from the couplings
and reproduces the manuscript to full precision (`kappa = 0.19748234`). Prefer the built-ins
for anything quantitative.

```python
from signedctx import level1, level2

level1("planck").kappa       # 0.19748234
level2("planck").kappa       # 0.63654275
level1("electroweak").kappa  # 0.00205758
```

---

## Demonstrating the two blindnesses

```python
from signedctx import decomposition_blindness, sign_blindness

report = decomposition_blindness(context, power=2)
report["identical"]     # True
report["kappa_real"]    # 0.1975  (resolved decomposition)
report["kappa_naive"]   # 0.0     (single channel, same net)

flip = sign_blindness(context, power=2)
flip["identical"]                    # True  -- reads |net| only
flip["kappa_invariant_under_flip"]   # True

sign_blindness(context, power=1)["identical"]   # False -- an odd observable sees the sign
```

The resolved and single-channel contexts have the same net, so an observable proportional to
`net²` assigns them the same value. It is blind both to the decomposition and to the sign.

---

## Comparing two resolutions

A gauge-factor decomposition and a gauge-boson/matter refinement have the same net but
different gross magnitudes and cancellation indices.

```python
from signedctx import level1, level2, refinement_report

d1, d2 = level1("planck"), level2("planck")
rep = refinement_report(d1, d2, groups=[[0], [1, 2], [3, 4]])

rep["net_invariant"]         # True
rep["gross_non_decreasing"]  # True   0.003840 -> 0.008479
rep["kappa_non_decreasing"]  # True   0.1975   -> 0.6365
rep["sign_homogeneous"]      # False  -- which is why kappa rose
```

The unchanged net is what a net-only amplitude reads. The change in gross and `kappa` records
structure the amplitude cannot resolve.

---

## Command-line use

```bash
python signedctx.py                       # full validation against the manuscript
python signedctx.py --levels              # both resolutions side by side
python signedctx.py --levels --scale electroweak
python signedctx.py --values 0.5 -0.3 0.2 --labels a b c
```

`--validate` (the default with no arguments) reproduces the manuscript's tables and checks the
monotonicity theorem, the two blindnesses, the edge cases, and the tilt value, asserting each.

Run the tests with:

```bash
pytest tests -q
```

---

## Citation

Please cite the manuscript revision accompanying this repository:

> De Jesús, Elias. (2026). *Two Blind Observables on a Signed Gauge Decomposition: An
> Invariance-Audited Diagnostic Reading of the Turok–Boyle Primordial Spectrum.* Zenodo.
> <https://doi.org/10.5281/zenodo.21780964>

The earlier version is superseded:

> De Jesús, Elias. (2026). *Amplitude–Tilt Complementarity and the Gauge Trace Anomaly as a
> Signed Context Decomposition: A Partition-Diagnostic Reading of the Turok–Boyle Primordial
> Spectrum.* Zenodo. <https://doi.org/10.5281/zenodo.20701311>

Please also cite the underlying physical proposal:

> N. Turok and L. Boyle. *A Minimal Explanation of the Primordial Cosmological Perturbations.*
> arXiv:2302.00344 [hep-ph] (2023).

A `CITATION.cff` file is included for GitHub's citation widget.

---

## License

Code in this repository is released under the MIT License; see `LICENSE`. The manuscript is
archived separately on Zenodo under the license specified in its deposition record.

# Signed Context Decomposition

Reference implementation accompanying the technical note

> **Amplitude–Tilt Complementarity and the Gauge Trace Anomaly as a Signed Context Decomposition:
> A Partition-Diagnostic Reading of the Turok–Boyle Primordial Spectrum**
> Elias De Jesús (2026)

- **Archived manuscript version accompanying this repository:** <https://doi.org/10.5281/zenodo.20701311>
- **Latest manuscript revision (resolves to the newest version):** <https://doi.org/10.5281/zenodo.20681973>

This is a scientific software repository, not a software product. It exists so that the
computational content of the note — the exact invariants of a signed context and the
algebraic blindness of a net-only observable — can be read, checked, and re-run.

---

## Overview

A **signed context** is a short vector of signed channel contributions `c_i` that sum to an
observable marginal. The module computes the three exact invariants of such a vector:

| quantity | definition | meaning |
|---|---|---|
| `net` | `Σ c_i` | the signed total; the only thing a net-only observable reads |
| `gross` | `Σ |c_i|` | the total magnitude mobilized across channels |
| `kappa` | `1 − |net| / gross` | the fraction of the gross magnitude that cancels |

`kappa = 0` means no cancellation (all channels share a sign); values approaching 1 mean a
small net conceals a large, sign-opposed structure. An equivalent form,
`kappa = 2·min(P, N) / gross` with `P` and `N` the positive and negative masses, is checked
numerically by the validation routine.

## Scientific motivation

Turok and Boyle ([arXiv:2302.00344](https://arxiv.org/abs/2302.00344)) source both the scalar
amplitude and the spectral tilt of the primordial perturbations from the high-temperature
trace-anomaly coefficient of the Standard Model. That coefficient is a sum of three
gauge-sector contributions,

```
c_beta = c_U(1) + c_SU(2) + c_SU(3)
```

and the contributions enter with **mixed signs**: at the Planck-scale couplings reported
there, hypercharge is positive while the weak and strong contributions are negative. The
strong channel dominates the net, while hypercharge and weak are sign-opposed and partially
cancel, giving `kappa ≈ 0.20` — about a fifth of the gross gauge magnitude cancels in the net
(Table 1 of the note).

Two consequences are implemented here.

1. **Signed marginal-blindness.** The amplitude depends on `c_beta` only through the net,
   `P_R ∝ net²`. It therefore cannot read `gross` or `kappa`: a net remainder produced by the
   near-cancellation of two sizeable, sign-opposed contributions is indistinguishable, at the
   level of the amplitude, from a single small contribution of the same net.
2. **A signed `L¹` structure is not a Fisher simplex.** Because the contributions are signed,
   the vector is not a probability simplex, and the Fisher-geometric content of the context
   resolver's marginal-blindness theorem (which requires `c_i ≥ 0`) does not apply. The
   blindness statement above is *algebraic*, not geometric. `classify_structure()` enforces
   this distinction and refuses to treat mixed-sign input as a simplex.

### What is exact, and what is not

- **Exact.** `net`, `gross`, `kappa`, the two equivalent forms of `kappa`, and the blindness of
  any observable of the form `O ∝ net^k`. These are algebraic identities; the code only
  evaluates them.
- **Exploratory (Tier 3).** `ensemble_kappa_statistics()` reports whether `kappa` clusters or
  spreads across an ensemble of decompositions (for example competing unification or
  beyond-Standard-Model completions). A single physical system cannot populate such an
  ensemble, so for the trace anomaly only the exact triple is defined. This diagnostic
  certifies nothing.

### Non-claims

This repository computes exact invariants of a given signed vector and nothing more. It does
not validate, derive, extend, or critique the Turok–Boyle construction, asserts no physical
mechanism, and proposes no new cosmology. All physical inputs are those reported in
[arXiv:2302.00344](https://arxiv.org/abs/2302.00344).

## Repository organization

```
README.md                 this file
LICENSE                   MIT license (code)
CITATION.cff              citation metadata, pinned to the archived manuscript version
requirements.txt          dependencies
paper/                    pointers to the manuscript archived on Zenodo
src/
    signedctx.py          the reference implementation
examples/
    01_trace_anomaly.py           reproduce Table 1
    02_marginal_blindness.py      two contexts, same net, same observable
    03_structure_and_ensemble.py  structural guard and the Tier 3 diagnostic
tests/
    test_signedctx.py     unit tests
```

The manuscript itself is archived on Zenodo rather than committed here; see `paper/README.md`.

## Installation

Python 3.9 or newer and NumPy are all that is required.

```bash
git clone https://github.com/<user>/signed-context-decomposition.git
cd signed-context-decomposition
pip install -r requirements.txt
```

No packaging step is needed. Scripts add `src/` to `sys.path`; if importing from elsewhere,
either do the same or set `PYTHONPATH=src`.

## Usage

```python
import sys; sys.path.insert(0, "src")
from signedctx import decompose

# Planck-scale gauge contributions to the trace-anomaly coefficient.
context = decompose(
    ["U(1)_Y", "SU(2)_L", "SU(3)_c"],
    [+0.00038, -0.00054, -0.00292],
)

print(context.net)               # -0.00308   what the amplitude reads
print(context.gross)             #  0.00384   total magnitude mobilized
print(context.kappa)             #  0.1979    fraction that cancels
print(context.dominant_channel)  # 'SU(3)_c'
print(context.summary())         # full report
```

Show that a net-only observable cannot see the cancellation:

```python
from signedctx import amplitude_blindness

report = amplitude_blindness(context, power=2)   # P_R ∝ net²
report["observables_identical"]                  # True
report["kappa_resolved"], report["kappa_single_channel"]   # (0.198, 0.0)
```

From the command line:

```bash
python src/signedctx.py                                 # reproduce and check Table 1
python src/signedctx.py --values 0.5 -0.3 0.2 --labels a b c
```

Run the examples and the tests:

```bash
python examples/01_trace_anomaly.py
pytest tests -q
```

## Citation

If you use this software, please cite the manuscript. `CITATION.cff` is pinned to the archived
version that this repository accompanies:

> De Jesús, Elias (2026). *Amplitude–Tilt Complementarity and the Gauge Trace Anomaly as a
> Signed Context Decomposition: A Partition-Diagnostic Reading of the Turok–Boyle Primordial
> Spectrum.* Zenodo. https://doi.org/10.5281/zenodo.20701311

To cite whichever revision is current instead, use the concept DOI
<https://doi.org/10.5281/zenodo.20681973>.

Please also cite the underlying physical result:

> N. Turok and L. Boyle, *A Minimal Explanation of the Primordial Cosmological Perturbations*,
> arXiv:2302.00344 [hep-ph] (2023).

## License

Code in this repository is released under the MIT License (see `LICENSE`). The manuscript is
archived separately on Zenodo under its own license.

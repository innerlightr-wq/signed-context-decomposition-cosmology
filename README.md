Signed Context Decomposition

Reference implementation accompanying the technical note

Two Blind Observables on a Signed Gauge Decomposition:
An Invariance-Audited Diagnostic Reading of the Turok–Boyle Primordial Spectrum
Elias De Jesús (2026)

* Latest manuscript revision accompanying this repository: https://doi.org/10.5281/zenodo.21780964
* Earlier manuscript version, now superseded: https://doi.org/10.5281/zenodo.20701311

This is a scientific software repository, not a software product. It exists so that the computational content of the note can be inspected, checked, and rerun.

The repository evaluates signed decompositions, tests the invariance properties of their summary quantities, and demonstrates the algebraic blindness of observables that depend only on a signed net.

⸻

Overview

A signed context is a finite vector of signed channel contributions (c_i). The module computes three descriptors:

Quantity	Definition	Meaning
net	Σ c_i	The signed total
gross	`Σ	c_i
kappa	`1 −	net

Writing

P = sum of positive contributions
N = absolute sum of negative contributions

the cancellation index also satisfies

kappa = 2·min(P, N) / (P + N)

This equivalent form is checked by the validation routines.

Interpretation:

* kappa = 0 means that all nonzero channels have the same sign.
* 0 < kappa < 1 indicates partial cancellation.
* kappa = 1 corresponds to exact cancellation, net = 0, provided gross > 0.

A central conclusion of the revised manuscript is that kappa is not a decomposition-free property of a physical system. It is a descriptor of a specified decomposition at a specified renormalization scale and perturbative truncation.

⸻

Scientific motivation

Turok and Boyle use the high-temperature Standard Model trace-anomaly coefficient

c_beta =
    (125/108) α_Y²
  − (95/72)  α_2²
  − (49/6)   α_3²

in their proposed account of the primordial scalar spectrum.

At the Planck-scale couplings quoted in their work, the three gauge-factor contributions have the sign pattern

U(1)_Y    positive
SU(2)_L   negative
SU(3)_c   negative

The weak and strong contributions therefore have the same sign. Only the hypercharge contribution is positive.

At this gauge-factor resolution, the values are approximately

net   = −0.003082
gross =  0.003840
kappa =  0.1975

The strong channel supplies about 95% of the magnitude of the net.

The revised note studies two different forms of observable blindness.

1. Amplitude blindness

The scalar amplitude is proportional to the square of the trace-anomaly coefficient:

P_R ∝ c_beta²

It therefore reads only the magnitude of the net signed sum.

It is blind to:

* the internal channel decomposition;
* the gross magnitude;
* the cancellation index;
* the overall sign of c_beta.

Two decompositions with equal net produce the same amplitude, regardless of how much sign-opposed structure lies underneath that net.

2. Tilt blindness

Under the heuristic wavelength-to-running assumptions used by Turok and Boyle, the spectral tilt reads the dominant (SU(3)) running combination rather than the full three-channel coefficient.

It is therefore insensitive to:

* the positive prefactor multiplying the dominant channel;
* the (U(1)_Y) channel;
* the (SU(2)_L) channel;
* the complete signed decomposition.

The amplitude and tilt are thus not complementary partition coordinates. They are better described as two different projections of a nested, two-level structure.

⸻

Two decomposition levels

The gauge-factor contributions can be written algebraically as

c_a = −P_a α_a² b_a

where P_a > 0 and

b_a = (11/3) C_A − (4/3) S_F

is the one-loop beta-function combination.

The positive factors are

P_U(1)  = 25/144
P_SU(2) = 19/48
P_SU(3) = 7/6

and the beta-function combinations are

b_U(1)  = −20/3
b_SU(2) =  10/3
b_SU(3) =  7

Because P_a and α_a² are positive, the sign of each gauge-factor contribution is carried by −b_a.

The (U(1)_Y) term is positive because an abelian gauge factor has no gauge self-interaction contribution, leaving the matter-screening part. The two non-abelian terms are negative because gauge-boson antiscreening dominates.

Level 1: gauge factors

U(1)_Y
SU(2)_L
SU(3)_c

At the Planck scale:

net   ≈ −0.003082
gross ≈  0.003840
kappa ≈  0.1975

Level 2: gauge-boson and matter pieces

Resolving each beta-function combination into gauge-boson and matter contributions gives

U(1)_Y matter
SU(2)_L gauge
SU(2)_L matter
SU(3)_c gauge
SU(3)_c matter

At this finer resolution:

net   ≈ −0.003082
gross ≈  0.008479
kappa ≈  0.6365

The net remains unchanged, while the gross magnitude and cancellation index increase.

Neither value of kappa is universally “the correct one.” Each describes a specified resolution.

⸻

Invariance audit

The revised manuscript proves the following refinement properties.

Suppose a contribution is split into smaller pieces whose sum equals the original contribution.

Quantities preserved under every refinement

The signed net is unchanged:

net_refined = net_original

Sign-homogeneous refinement

When every child contribution has the same sign as its parent:

gross_refined = gross_original
kappa_refined = kappa_original

Examples include:

* relabeling channels;
* splitting a positive channel into positive pieces;
* splitting a negative channel into negative pieces;
* merging channels of the same sign.

Sign-crossing refinement

When a channel is split into pieces of opposite sign:

gross_refined > gross_original
kappa_refined > kappa_original

Consequently, kappa is monotone non-decreasing under refinement.

Merging opposite-sign channels has the reverse effect and decreases kappa.

No decomposition-free value

For a fixed nonzero net, decompositions can be constructed with kappa arbitrarily close to 1. Coarsening the entire vector into a single channel gives kappa = 0.

Therefore:

kappa is a resolution-relative coordinate,
not an invariant of the underlying physical system.

⸻

Scale and truncation dependence

The channel values depend on the renormalization scale through the running couplings.

Using the same leading expression:

Scale	Approximate kappa
Planck scale	0.197
Electroweak scale	0.002

The electroweak calculation is illustrative only. It applies the same high-temperature expression at a scale where its physical applicability and perturbative hierarchy differ.

The decomposition is also tied to perturbative order. At higher orders, mixed-coupling terms can involve more than one gauge factor. Such terms require either:

* additional interaction channels; or
* an explicit convention assigning them to existing channels.

The channel list is therefore itself part of the stated analytical resolution.

⸻

What is exact, interpretive, and not claimed

Exact algebra

The repository directly evaluates or checks:

* net;
* gross;
* kappa;
* the equivalent positive/negative-mass form of kappa;
* invariance under relabeling;
* invariance under sign-homogeneous refinement;
* monotonicity under sign-crossing refinement;
* decomposition blindness of observables O = f(net);
* additional sign blindness when f is even;
* the level-1 and level-2 numerical decompositions.

Imported physical statements

The amplitude relation and the proposed tilt relation belong to the Turok–Boyle framework.

Their tilt analysis is explicitly heuristic and depends on assumptions connecting spatial wavelength to renormalization-group running. This repository does not strengthen the epistemic status of that argument.

Structural interpretation

The following are diagnostic interpretations rather than physical results:

* amplitude and tilt as two different blindnesses;
* kappa as a resolution-depth coordinate;
* the level-1-to-level-2 change in kappa as a measure of sign structure hidden by a coarser labeling.

Non-claims

This repository does not:

* validate the Turok–Boyle construction;
* derive the primordial spectrum;
* extend or critique their physical mechanism;
* establish a new cosmological model;
* treat kappa ≈ 0.20 as a Standard Model constant;
* attach physical significance to its numerical proximity to (1/5);
* identify a mixed-sign vector with a Fisher probability simplex.

⸻

Signed (L^1) structure is not a Fisher simplex

The gauge contributions have mixed signs. They therefore do not form a probability simplex.

The context-resolver framework for positive components assumes

c_i ≥ 0

and uses Fisher information geometry on a normalized positive composition. Those assumptions do not hold here.

The present blindness statement is purely algebraic:

an observable that depends only on the sum
cannot resolve the terms inside that sum.

Normalizing the absolute values would create a positive simplex, but it would discard the sign information that motivates this analysis.

The software therefore distinguishes mixed-sign structures from positive simplex-like inputs and does not silently apply Fisher-geometric interpretations to signed data.

⸻

Repository organization

The repository may contain the following files and directories:

README.md
LICENSE
CITATION.cff
requirements.txt
signedctx.py

In versions organized as a Python source tree, the implementation and supporting material may instead appear as:

src/
    signedctx.py
examples/
    01_trace_anomaly.py
    02_marginal_blindness.py
    03_structure_and_ensemble.py
tests/
    test_signedctx.py
paper/
    README.md

The manuscript is archived on Zenodo rather than committed as the authoritative publication file.

Before running the commands below, use the path matching the organization of the checked-out repository.

⸻

Installation

Python 3.9 or newer and NumPy are required.

git clone https://github.com/innerlightr-wq/signed-context-decomposition-cosmology.git
cd signed-context-decomposition-cosmology
pip install -r requirements.txt

No packaging step is required.

For a root-level implementation:

from signedctx import decompose

For a src/ layout:

import sys
sys.path.insert(0, "src")
from signedctx import decompose

⸻

Basic usage

from signedctx import decompose
context = decompose(
    ["U(1)_Y", "SU(2)_L", "SU(3)_c"],
    [+0.0003792, -0.0005437, -0.0029170],
)
print(context.net)
# approximately -0.003082
print(context.gross)
# approximately 0.003840
print(context.kappa)
# approximately 0.1975
print(context.dominant_channel)
# SU(3)_c
print(context.summary())

⸻

Demonstrating decomposition blindness

from signedctx import amplitude_blindness
report = amplitude_blindness(context, power=2)
print(report["observables_identical"])
# True
print(report["kappa_resolved"])
# approximately 0.1975
print(report["kappa_single_channel"])
# 0.0

The resolved and single-channel contexts have the same net, so an observable proportional to net² assigns them the same value.

The observable is blind both to the decomposition and to the sign of the net.

⸻

Comparing two resolutions

A gauge-factor decomposition and a gauge-boson/matter refinement can have the same net but different gross magnitudes and cancellation indices.

level_1 = [
    +0.0003792,
    -0.0005437,
    -0.0029170,
]
level_2 = [
    +0.0003792,  # U(1) matter
    -0.0011960,  # SU(2) gauge
    +0.0006525,  # SU(2) matter
    -0.0045840,  # SU(3) gauge
    +0.0016670,  # SU(3) matter
]

Expected values:

Level 1:
net   ≈ −0.003082
gross ≈  0.003840
kappa ≈  0.1975
Level 2:
net   ≈ −0.003082
gross ≈  0.008479
kappa ≈  0.6365

The unchanged net is what a net-only amplitude reads. The change in gross and kappa records structure that the amplitude cannot resolve.

⸻

Command-line use

For a root-level script:

python signedctx.py
python signedctx.py --values 0.5 -0.3 0.2 --labels a b c

For a src/ layout:

python src/signedctx.py
python src/signedctx.py --values 0.5 -0.3 0.2 --labels a b c

Run tests, when included, with:

pytest tests -q

⸻

Citation

Please cite the latest manuscript revision:

De Jesús, Elias. (2026). Two Blind Observables on a Signed Gauge Decomposition: An Invariance-Audited Diagnostic Reading of the Turok–Boyle Primordial Spectrum. Zenodo. https://doi.org/10.5281/zenodo.21780964

The earlier manuscript version is superseded:

De Jesús, Elias. (2026). Amplitude–Tilt Complementarity and the Gauge Trace Anomaly as a Signed Context Decomposition: A Partition-Diagnostic Reading of the Turok–Boyle Primordial Spectrum. Zenodo. https://doi.org/10.5281/zenodo.20701311

Please also cite the underlying physical proposal:

N. Turok and L. Boyle. A Minimal Explanation of the Primordial Cosmological Perturbations. arXiv:2302.00344 [hep-ph] (2023).

⸻

License

Code in this repository is released under the MIT License. See LICENSE.

The manuscript is archived separately on Zenodo under the license specified in its deposition record.

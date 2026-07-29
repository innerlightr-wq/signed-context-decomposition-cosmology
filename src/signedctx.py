"""Signed context decomposition analyzer.

Reference implementation for:

    E. De Jesus, "Amplitude-Tilt Complementarity and the Gauge Trace Anomaly
    as a Signed Context Decomposition: A Partition-Diagnostic Reading of the
    Turok-Boyle Primordial Spectrum" (2026).
    https://doi.org/10.5281/zenodo.20701311

A *signed context* is a short vector of signed channel contributions ``c_i``
that sum to an observable marginal.  The motivating case is the
high-temperature trace-anomaly coefficient of the Standard Model,

    c_beta = c_U(1) + c_SU(2) + c_SU(3),

whose three gauge-sector contributions enter with mixed signs.  The scalar
amplitude of the Turok-Boyle construction reads only the *net* sum, and is
therefore blind to the *gross* magnitude that was mobilized and to how much
sign-opposed structure cancelled inside it.

What is exact and what is not
-----------------------------
EXACT (algebraic identities; this module only evaluates them)

    net    = sum_i c_i
    gross  = sum_i |c_i|
    kappa  = 1 - |net| / gross          cancellation index, in [0, 1)
    kappa  = 2 * min(P, N) / gross      P, N = positive / negative masses

    The two expressions for ``kappa`` are the same quantity;
    :func:`validate_against_paper` asserts their agreement numerically.

EXACT (marginal-blindness, algebraic).  An observable of the form
``O ~ net**k`` -- for instance the scalar amplitude ``P_R ~ net**2`` -- is a
function of the signed sum alone.  It cannot see ``gross`` or ``kappa``: a
small net assembled from large sign-opposed channels is indistinguishable
from a single small channel of the same net.  :func:`amplitude_blindness`
exhibits this explicitly.

NOT A FISHER SIMPLEX.  Signed input is not a probability simplex, so the
context resolver's warped-product marginal-blindness theorem -- which
requires ``c_i >= 0`` -- does not apply.  :func:`classify_structure` enforces
the distinction and refuses to treat mixed-sign input as a simplex.  The
blindness statement above is algebraic, not Fisher-geometric.

EXPLORATORY, Tier 3.  Given an ensemble of decompositions (e.g. competing
beyond-Standard-Model completions), :func:`ensemble_kappa_statistics` reports
whether ``kappa`` clusters or spreads.  A single physical system cannot
populate such an ensemble, so for the paper's Table 1 only the exact triple
``(net, gross, kappa)`` is defined.  This diagnostic certifies nothing.

Non-claims
----------
This module computes exact invariants of a given signed vector and nothing
more.  It does not validate, derive, or extend the Turok-Boyle construction,
asserts no physical mechanism, and the ensemble diagnostic is not a theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

__all__ = [
    "POSITIVE_SIMPLEX",
    "SIGNED_L1",
    "STRUCTURE_NOTES",
    "TRACE_ANOMALY",
    "Decomposition",
    "amplitude_blindness",
    "classify_structure",
    "decompose",
    "ensemble_kappa_statistics",
    "net_gross_kappa",
    "positive_negative_masses",
    "validate_against_paper",
]

#: Below this total magnitude the context is treated as all-zero and ``kappa``
#: is undefined (the ratio ``|net| / gross`` has no meaning).
ZERO_GROSS_TOLERANCE = 1e-300

# Structure labels returned by classify_structure().
POSITIVE_SIMPLEX = "positive_simplex"
SIGNED_L1 = "signed_l1"

STRUCTURE_NOTES = {
    POSITIVE_SIMPLEX: (
        "positive simplex: after normalization the resolver's Fisher "
        "marginal-blindness theorem applies"
    ),
    SIGNED_L1: (
        "signed L1: not a probability simplex, so the resolver's Fisher "
        "theorem does not apply -- use net / gross / kappa instead"
    ),
}


# ---------------------------------------------------------------------------
# Core exact invariants of a signed L1 decomposition
# ---------------------------------------------------------------------------
def net_gross_kappa(values: Sequence[float]) -> tuple[float, float, float]:
    """Return the exact triple ``(net, gross, kappa)`` of a signed context.

    Parameters
    ----------
    values
        Signed channel contributions ``c_i``.

    Returns
    -------
    net, gross, kappa
        ``net = sum(c_i)``, ``gross = sum(|c_i|)`` and the cancellation index
        ``kappa = 1 - |net| / gross``.  For an all-zero context the triple is
        ``(0.0, 0.0, nan)``: no magnitude was mobilized, so the fraction that
        cancels is undefined.

    Notes
    -----
    ``kappa = 0`` means no cancellation (all contributions share a sign);
    values approaching 1 mean a small net conceals a large sign-opposed
    gross structure.
    """
    contributions = np.asarray(values, dtype=float)
    net = float(contributions.sum())
    gross = float(np.abs(contributions).sum())
    if gross < ZERO_GROSS_TOLERANCE:
        return 0.0, 0.0, float("nan")
    return net, gross, 1.0 - abs(net) / gross


def positive_negative_masses(values: Sequence[float]) -> tuple[float, float]:
    """Return ``(P, N)``: the positive mass and the negative mass.

    ``P`` is the sum of the positive contributions and ``N`` the sum of the
    absolute values of the negative ones, so ``net = P - N`` and
    ``gross = P + N``.
    """
    contributions = np.asarray(values, dtype=float)
    positive_mass = float(contributions[contributions > 0].sum())
    negative_mass = float(-contributions[contributions < 0].sum())
    return positive_mass, negative_mass


@dataclass(frozen=True)
class Decomposition:
    """Exact invariants of one signed context.

    Attributes
    ----------
    channels
        Channel labels, in input order.
    values
        Signed contributions ``c_i``.
    net
        Signed sum -- the only thing a net-only observable reads.
    gross
        Total mobilized magnitude ``sum(|c_i|)``.
    kappa
        Cancellation index ``1 - |net| / gross``; ``nan`` if ``gross == 0``.
    positive_mass, negative_mass
        ``P`` and ``N`` as defined in :func:`positive_negative_masses`.
    dominant_channel, dominant_fraction
        Largest channel by ``|c_i|`` and its share ``|c_dom| / gross``.
    signs
        Sign pattern, e.g. ``('+', '-', '-')``.
    structure
        :data:`POSITIVE_SIMPLEX` or :data:`SIGNED_L1`.
    """

    channels: tuple[str, ...]
    values: np.ndarray
    net: float
    gross: float
    kappa: float
    positive_mass: float
    negative_mass: float
    dominant_channel: str
    dominant_fraction: float
    signs: tuple[str, ...]
    structure: str

    def as_dict(self) -> dict:
        """Return a plain, JSON-serializable dictionary of the invariants."""
        return {
            "channels": list(self.channels),
            "values": [float(v) for v in self.values],
            "net": self.net,
            "gross": self.gross,
            "kappa": self.kappa,
            "positive_mass": self.positive_mass,
            "negative_mass": self.negative_mass,
            "dominant_channel": self.dominant_channel,
            "dominant_fraction": self.dominant_fraction,
            "signs": list(self.signs),
            "structure": self.structure,
        }

    def summary(self) -> str:
        """Return a human-readable multi-line report."""
        rows = "\n".join(
            f"    {channel:<10s} {value:+.6g}   ({sign})"
            for channel, value, sign in zip(self.channels, self.values, self.signs)
        )
        return (
            f"channels:\n{rows}\n"
            f"  net      = {self.net:+.6g}      <- a net-only observable reads this\n"
            f"  gross    = {self.gross:.6g}\n"
            f"  P (pos)  = {self.positive_mass:.6g}   "
            f"N (neg) = {self.negative_mass:.6g}\n"
            f"  kappa    = {self.kappa:.4f}       <- fraction of gross that cancels\n"
            f"  dominant = {self.dominant_channel} "
            f"({self.dominant_fraction:.3f} of gross)\n"
            f"  structure= {STRUCTURE_NOTES[self.structure]}"
        )


def decompose(channels: Sequence[str], values: Sequence[float]) -> Decomposition:
    """Compute every exact invariant of a signed context.

    Parameters
    ----------
    channels
        Channel labels.
    values
        Signed contributions, same length as ``channels``.

    Raises
    ------
    ValueError
        If the two arguments have different lengths, or are empty.
    """
    contributions = np.asarray(values, dtype=float)
    if len(channels) != len(contributions):
        raise ValueError(
            f"channels and values length mismatch: "
            f"{len(channels)} != {len(contributions)}"
        )
    if contributions.size == 0:
        raise ValueError("a decomposition needs at least one channel")

    net, gross, kappa = net_gross_kappa(contributions)
    positive_mass, negative_mass = positive_negative_masses(contributions)

    dominant_index = int(np.argmax(np.abs(contributions)))
    dominant_fraction = (
        float(abs(contributions[dominant_index]) / gross)
        if gross >= ZERO_GROSS_TOLERANCE
        else float("nan")
    )
    signs = tuple(
        "+" if value > 0 else "-" if value < 0 else "0" for value in contributions
    )

    return Decomposition(
        channels=tuple(channels),
        values=contributions,
        net=net,
        gross=gross,
        kappa=kappa,
        positive_mass=positive_mass,
        negative_mass=negative_mass,
        dominant_channel=channels[dominant_index],
        dominant_fraction=dominant_fraction,
        signs=signs,
        structure=classify_structure(contributions),
    )


# ---------------------------------------------------------------------------
# Structural guard: a signed L1 context is not a Fisher simplex
# ---------------------------------------------------------------------------
def classify_structure(values: Sequence[float]) -> str:
    """Decide whether the resolver's positive-context theorem can apply.

    Returns :data:`POSITIVE_SIMPLEX` when every contribution is
    non-negative -- the vector can then be normalized and the resolver's
    Fisher marginal-blindness theorem applies -- and :data:`SIGNED_L1` when
    any contribution is negative, in which case that theorem does not apply
    and the invariants of interest are ``net``, ``gross`` and ``kappa``.

    See :data:`STRUCTURE_NOTES` for the corresponding prose descriptions.
    """
    contributions = np.asarray(values, dtype=float)
    if np.all(contributions >= 0):
        return POSITIVE_SIMPLEX
    return SIGNED_L1


# ---------------------------------------------------------------------------
# Marginal-blindness: a net-only observable cannot see gross or kappa
# ---------------------------------------------------------------------------
def amplitude_blindness(decomposition: Decomposition, power: int = 2) -> dict:
    """Exhibit the blindness of an observable ``O ~ net**power``.

    Builds the "naive" single-channel context carrying the *same net* (and
    hence ``kappa = 0``, no cancellation) and confirms that the observable is
    numerically identical while the cancellation structure is not.  This is
    the signed analogue of the resolver's marginal-blindness, stated
    algebraically rather than Fisher-geometrically.

    Parameters
    ----------
    decomposition
        The real, resolved context.
    power
        Exponent of the net in the observable; ``2`` for the scalar
        amplitude ``P_R ~ c_net**2``.

    Returns
    -------
    dict
        The two observable values, a boolean flag recording that they agree,
        and the ``kappa`` / ``gross`` pair that the observable cannot see.
    """
    observable_resolved = decomposition.net**power
    naive = decompose(["net_only"], [decomposition.net])
    observable_naive = naive.net**power
    scale = max(1.0, abs(observable_resolved))
    return {
        "observable_power": power,
        "observable_resolved": observable_resolved,
        "observable_single_channel": observable_naive,
        "observables_identical": bool(
            abs(observable_resolved - observable_naive) < 1e-18 * scale
        ),
        "kappa_resolved": decomposition.kappa,
        "kappa_single_channel": naive.kappa,
        "gross_resolved": decomposition.gross,
        "gross_single_channel": naive.gross,
        "reading": (
            "identical observable, different cancellation: the net-only "
            "observable cannot distinguish the two contexts"
        ),
    }


# ---------------------------------------------------------------------------
# Ensemble mode (Tier 3, exploratory)
# ---------------------------------------------------------------------------
def ensemble_kappa_statistics(decompositions: Sequence[Decomposition]) -> dict:
    """Summarize the spread of ``kappa`` across an ensemble of contexts.

    Reports mean, sample standard deviation and coefficient of variation as a
    crude clusters-versus-spreads read.  This is *not* a theorem: it is
    meaningful only for genuinely independent samples (for example competing
    unification or beyond-Standard-Model completions), and a single physical
    system cannot populate it.  Contexts with zero gross are skipped, since
    their ``kappa`` is undefined.
    """
    kappas = np.array(
        [d.kappa for d in decompositions if not np.isnan(d.kappa)], dtype=float
    )
    if kappas.size == 0:
        return {"n": 0, "note": "no valid (nonzero-gross) decompositions"}

    nets = np.array([d.net for d in decompositions], dtype=float)
    grosses = np.array([d.gross for d in decompositions], dtype=float)

    mean = float(kappas.mean())
    std = float(kappas.std(ddof=1)) if kappas.size > 1 else 0.0
    coefficient_of_variation = std / mean if mean > 0 else float("nan")

    return {
        "n": int(kappas.size),
        "kappa_mean": round(mean, 4),
        "kappa_std": round(std, 4),
        "kappa_cv": (
            None
            if np.isnan(coefficient_of_variation)
            else round(coefficient_of_variation, 4)
        ),
        "net_range": (round(float(nets.min()), 6), round(float(nets.max()), 6)),
        "gross_range": (round(float(grosses.min()), 6), round(float(grosses.max()), 6)),
        "read": (
            "small cv -> kappa clusters, a candidate structural invariant; "
            "large cv -> kappa spreads, so the index is a useful frame rather "
            "than a constant. Tier 3 exploratory; needs independent completions."
        ),
    }


# ---------------------------------------------------------------------------
# Validation against the paper (Table 1)
# ---------------------------------------------------------------------------
#: Planck-scale gauge-sector contributions to the trace-anomaly coefficient
#: c_beta, as reported in Table 1 of the accompanying note.  The underlying
#: Standard Model inputs are those of Turok and Boyle, arXiv:2302.00344.
TRACE_ANOMALY = {
    "channels": ["U(1)_Y", "SU(2)_L", "SU(3)_c"],
    "values": [+0.00038, -0.00054, -0.00292],
    "paper_net": -0.00308,
    "paper_gross": 0.00384,
    "paper_kappa": 0.20,
}


def validate_against_paper(verbose: bool = True) -> Decomposition:
    """Reproduce Table 1 of the paper and check the internal identities.

    Prints five checks: the reported net, gross and ``kappa``; the agreement
    of the two algebraic forms of ``kappa``; the dominant channel; the
    structural guard firing on mixed-sign input; and the amplitude
    marginal-blindness.  Returns the trace-anomaly decomposition.
    """
    decomposition = decompose(TRACE_ANOMALY["channels"], TRACE_ANOMALY["values"])

    def flag(observed: float, expected: float, tolerance: float) -> str:
        return "OK" if abs(observed - expected) < tolerance else "??"

    if not verbose:
        return decomposition

    print("=== VALIDATION (Turok-Boyle trace anomaly, Table 1) ===")

    # (1) net / gross / kappa reproduce the reported values.
    print(
        f"net   = {decomposition.net:+.5f}   "
        f"paper {TRACE_ANOMALY['paper_net']:+.5f}   "
        f"{flag(decomposition.net, TRACE_ANOMALY['paper_net'], 5e-6)}"
    )
    print(
        f"gross = {decomposition.gross:.5f}   "
        f"paper {TRACE_ANOMALY['paper_gross']:.5f}   "
        f"{flag(decomposition.gross, TRACE_ANOMALY['paper_gross'], 5e-6)}"
    )
    print(
        f"kappa = {decomposition.kappa:.4f}    "
        f"paper {TRACE_ANOMALY['paper_kappa']:.2f}      "
        f"{flag(decomposition.kappa, TRACE_ANOMALY['paper_kappa'], 5e-3)}"
    )

    # (2) The two algebraic forms of kappa agree.
    kappa_from_masses = (
        2.0
        * min(decomposition.positive_mass, decomposition.negative_mass)
        / decomposition.gross
    )
    print(
        "kappa identity 1-|net|/gross == 2*min(P,N)/gross: "
        f"{decomposition.kappa:.10f} vs {kappa_from_masses:.10f}   "
        f"{flag(decomposition.kappa, kappa_from_masses, 1e-12)}"
    )

    # (3) The strong channel dominates the net.
    print(
        f"dominant channel = {decomposition.dominant_channel} at "
        f"{decomposition.dominant_fraction:.3f} of gross   "
        f"{'OK' if decomposition.dominant_channel == 'SU(3)_c' else '??'}"
    )

    # (4) The structural guard fires on mixed-sign input.
    print(f"structure: {STRUCTURE_NOTES[decomposition.structure]}")
    print(f"   guard OK: {'OK' if decomposition.structure == SIGNED_L1 else '??'}")

    # (5) Amplitude marginal-blindness.
    blindness = amplitude_blindness(decomposition, power=2)
    print(
        "amplitude blindness (P_R ~ net^2): identical observable across "
        f"kappa={blindness['kappa_resolved']:.2f} and "
        f"kappa={blindness['kappa_single_channel']:.2f}  "
        f"{'OK' if blindness['observables_identical'] else '??'}"
    )
    print()
    return decomposition


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------
def _build_argument_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Signed context decomposition analyzer"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="reproduce Table 1 of the accompanying paper",
    )
    parser.add_argument(
        "--values",
        type=float,
        nargs="*",
        help="signed channel contributions to analyze",
    )
    parser.add_argument(
        "--labels",
        type=str,
        nargs="*",
        help="optional channel labels (must match the number of --values)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Entry point: validate the paper's table, or analyze a custom context."""
    import json

    args = _build_argument_parser().parse_args(argv)

    if args.values:
        labels = args.labels or [f"c{i}" for i in range(len(args.values))]
        decomposition = decompose(labels, args.values)
        print(decomposition.summary())
        if args.validate:
            print()
            validate_against_paper()
        return

    decomposition = validate_against_paper()
    print("=== trace-anomaly decomposition ===")
    print(decomposition.summary())
    print()
    print("=== amplitude blindness ===")
    print(json.dumps(amplitude_blindness(decomposition), indent=2, default=str))


if __name__ == "__main__":
    main()

"""
signedctx.py  --  Signed Context Decomposition Analyzer  (v2)
=============================================================

Companion tool to

    De Jesus, "Two Blind Observables on a Signed Gauge Decomposition:
    An Invariance-Audited Diagnostic Reading of the Turok-Boyle Primordial
    Spectrum" (2026),

which supersedes "Amplitude-Tilt Complementarity and the Gauge Trace Anomaly
as a Signed Context Decomposition" (zenodo.20701311).  v1 of this tool tracked
the superseded note; the changes below are not cosmetic.

WHAT CHANGED FROM v1
--------------------
  1. The amplitude reads |net|, NOT the signed net.  P_R ~ net^2 is an EVEN
     function, so it is blind to the decomposition AND to the overall sign.
     These are logically independent blindnesses; both are exhibited here.
  2. kappa is NOT an invariant.  It is a descriptor of a stated resolution.
     Under refinement:  net is fixed, gross is non-decreasing, kappa is
     non-decreasing -- with equality exactly for sign-homogeneous refinement.
     Over all decompositions of a fixed nonzero net, kappa sweeps [0,1).
     This module now implements refinement and checks the monotonicity.
  3. Channel values are computed from Turok-Boyle Eq. (4) and the couplings,
     not hardcoded from a rounded table, so the scale dependence is live.
  4. A second resolution ("level 2") is provided: each gauge factor splits
     into gauge-boson (antiscreening) and matter (screening) pieces via the
     one-loop beta coefficient.  Same net, kappa 0.197 -> 0.637.

WHAT IS EXACT vs INTERPRETED
----------------------------
  * EXACT (algebra; this tool only evaluates it):
        net    = sum_i c_i
        gross  = sum_i |c_i|
        kappa  = 1 - |net|/gross  = 2*min(P,N)/gross,   in [0,1]
        kappa == 1 iff net == 0 (total cancellation); undefined if gross == 0.
  * EXACT (monotonicity, Thm 6.2 of the note): see refinement_report().
  * EXACT but near-trivial (marginal blindness): an observable f(net) cannot
     see gross or kappa; if f is even it also cannot see sign(net).  This is
     a remark about functions of a sum, not a result.  Do not cite it as one.
  * NOT A FISHER SIMPLEX: signed input is not a probability simplex, so the
     resolver's warped-product theorem (which needs c_i >= 0) does NOT apply.
     classify_structure() enforces the distinction.
  * ALGEBRAIC, NOT SOURCED PHYSICS: the factorization c_a = -P_a alpha_a^2 b_a
     holds for all three channels with P_a > 0, but Turok and Boyle interpret
     the positive factor thermally only for SU(3).  For U(1) and SU(2), P_a is
     defined here as a ratio.  No thermal identification is claimed.
  * EXPLORATORY (Tier 3): ensemble() varies the THEORY at fixed resolution.
     It says nothing about resolution dependence, which is settled formally by
     the monotonicity theorem.

NON-CLAIMS
----------
  This tool computes descriptors of a given signed vector at a given
  resolution.  It does not validate, derive, or extend the Turok-Boyle
  construction, asserts no physical mechanism, and produces no invariants of
  the Standard Model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

EPS = 1e-300  # guard against gross == 0 (all-zero context)


# ==========================================================================
# 1.  Core descriptors of a signed L1 decomposition
# ==========================================================================
@dataclass
class Decomposition:
    channels: list          # channel labels
    values: np.ndarray      # signed contributions c_i
    net: float              # sum_i c_i        -- fixed by theory+scale+truncation
    gross: float            # sum_i |c_i|      -- needs a stated resolution
    kappa: float            # 1 - |net|/gross  -- needs a stated resolution
    P: float                # positive mass  sum_{c_i>0} c_i
    N: float                # negative mass  sum_{c_i<0} |c_i|
    dom_ch: str             # dominant channel by |c_i|
    dom_frac: float         # |c_dom| / gross
    signs: tuple            # e.g. ('+','-','-')

    def summary(self) -> str:
        rows = "\n".join(
            f"    {c:<18s} {v:+.6e}   ({s})"
            for c, v, s in zip(self.channels, self.values, self.signs)
        )
        return (
            f"channels ({len(self.values)}):\n{rows}\n"
            f"  net      = {self.net:+.6e}   <- resolution-INVARIANT; |net| is what P_R reads\n"
            f"  gross    = {self.gross:.6e}   <- resolution-relative\n"
            f"  P (pos)  = {self.P:.6e}   N (neg) = {self.N:.6e}\n"
            f"  kappa    = {self.kappa:.6f}      <- resolution-relative, monotone under refinement\n"
            f"  dominant = {self.dom_ch} ({self.dom_frac:.3f} of gross)"
        )


def net_gross_kappa(values: Sequence[float]) -> tuple[float, float, float]:
    """Exact core.  kappa = 1 - |net|/gross in [0,1]; kappa == 1 iff net == 0."""
    v = np.asarray(values, dtype=float)
    net = float(v.sum())
    gross = float(np.abs(v).sum())
    if gross < EPS:
        return 0.0, 0.0, float("nan")      # all-zero context: kappa undefined
    return net, gross, 1.0 - abs(net) / gross


def sign_masses(values: Sequence[float]) -> tuple[float, float]:
    """P = sum of positive parts, N = sum of |negative parts|.  Zeros ignored."""
    v = np.asarray(values, dtype=float)
    return float(v[v > 0].sum()), float(-v[v < 0].sum())


def analyze(channels: Sequence[str], values: Sequence[float]) -> Decomposition:
    v = np.asarray(values, dtype=float)
    if len(channels) != len(v):
        raise ValueError("channels and values length mismatch")
    net, gross, kappa = net_gross_kappa(v)
    P, N = sign_masses(v)
    j = int(np.argmax(np.abs(v)))
    return Decomposition(
        channels=list(channels), values=v, net=net, gross=gross, kappa=kappa,
        P=P, N=N, dom_ch=channels[j],
        dom_frac=float(abs(v[j]) / gross) if gross >= EPS else float("nan"),
        signs=tuple("+" if x > 0 else "-" if x < 0 else "0" for x in v),
    )


def classify_structure(values: Sequence[float]) -> str:
    """Whether the resolver's positive-context (Fisher simplex) theorem applies."""
    v = np.asarray(values, dtype=float)
    if np.all(v >= 0):
        return "positive simplex (resolver Fisher theorem APPLIES after normalization)"
    return ("signed L1 (NOT a Fisher simplex; resolver theorem does NOT apply "
            "-- use net/gross/kappa and read blindness algebraically)")


# ==========================================================================
# 2.  Refinement, coarsening, and the monotonicity theorem
# ==========================================================================
def is_sign_homogeneous(pieces: Sequence[float], tol: float = 0.0) -> bool:
    """True iff no two NONZERO pieces have strictly opposite signs.

    Zeros are ignored: adjoining zero terms changes neither gross nor kappa.
    """
    p = np.asarray(pieces, dtype=float)
    nz = p[np.abs(p) > tol]
    return bool(nz.size == 0 or np.all(nz > 0) or np.all(nz < 0))


def refine(channels: Sequence[str], values: Sequence[float],
           index: int, pieces: Sequence[float],
           rtol: float = 1e-12) -> Decomposition:
    """Replace component `index` by `pieces`, which must sum to it.

    This is refinement in the sense of Definition 6.1 of the note: the pieces
    are ASSIGNED to the parent component and reproduce it.  Adjoining an
    unassigned (+X,-X) pair is NOT a refinement and is rejected elsewhere.
    """
    v = list(map(float, values))
    parent = v[index]
    total = float(np.sum(pieces))
    if abs(total - parent) > rtol * max(1.0, abs(parent)):
        raise ValueError(
            f"pieces sum to {total!r}, not to the parent component {parent!r}; "
            "this is not a refinement")
    lab = list(channels)
    new_lab, new_val = [], []
    for i, (c, x) in enumerate(zip(lab, v)):
        if i == index:
            for k, pc in enumerate(pieces):
                new_lab.append(f"{c}:{k}")
                new_val.append(float(pc))
        else:
            new_lab.append(c)
            new_val.append(x)
    return analyze(new_lab, new_val)


def coarsen(channels: Sequence[str], values: Sequence[float],
            groups: Sequence[Sequence[int]]) -> Decomposition:
    """Merge index groups (a partition of range(len(values))) into single channels."""
    v = np.asarray(values, dtype=float)
    seen = sorted(i for g in groups for i in g)
    if seen != list(range(len(v))):
        raise ValueError("groups must partition all component indices exactly once")
    lab = ["+".join(channels[i] for i in g) for g in groups]
    val = [float(v[list(g)].sum()) for g in groups]
    return analyze(lab, val)


def refinement_report(parent: Decomposition, child: Decomposition,
                      groups: Sequence[Sequence[int]] | None = None,
                      rtol: float = 1e-12) -> dict:
    """Check Theorem 6.2 (i)-(iii) numerically for a parent/child pair.

    (i)   net unchanged
    (ii)  gross non-decreasing, equality iff every group is sign-homogeneous
    (iii) kappa non-decreasing, equality under the same condition
    """
    scale = max(1.0, abs(parent.net))
    net_ok = abs(child.net - parent.net) <= rtol * scale
    homog = None
    if groups is not None:
        homog = all(is_sign_homogeneous(child.values[list(g)]) for g in groups)
    gross_eq = abs(child.gross - parent.gross) <= rtol * max(1.0, parent.gross)
    return {
        "net_invariant": bool(net_ok),
        "net": parent.net,
        "gross_parent": parent.gross,
        "gross_child": child.gross,
        "gross_non_decreasing": bool(child.gross >= parent.gross - rtol * max(1.0, parent.gross)),
        "kappa_parent": parent.kappa,
        "kappa_child": child.kappa,
        "kappa_non_decreasing": bool(child.kappa >= parent.kappa - 1e-12),
        "sign_homogeneous": homog,
        "equality_holds": bool(gross_eq),
        "equality_matches_homogeneity": None if homog is None else bool(gross_eq == homog),
    }


def kappa_span(values: Sequence[float], index: int = 0,
               Xs: Sequence[float] = (1e-3, 1e-2, 1e0, 1e3)) -> list[dict]:
    """Theorem 6.2(vi), constructive: refine c_r as (c_r + X, -X).

    Valid (i.e. sign-crossing) only for X > max(0, -c_r).  Below that threshold
    the refinement is sign-homogeneous and kappa is UNCHANGED -- which is the
    equality clause of (ii), and worth seeing rather than assuming.
    """
    v = list(map(float, values))
    c_r = v[index]
    threshold = max(0.0, -c_r)
    base = analyze([f"c{i}" for i in range(len(v))], v)
    out = []
    for X in Xs:
        d = refine(base.channels, v, index, [c_r + X, -X])
        out.append({
            "X": X, "threshold": threshold, "crosses_sign_boundary": bool(X > threshold),
            "net": d.net, "gross": d.gross, "kappa": d.kappa,
            "kappa_unchanged": bool(abs(d.kappa - base.kappa) < 1e-12),
        })
    return out


def realize_kappa(net: float, target_kappa: float) -> Decomposition:
    """Two-component decomposition with the given net realizing any kappa in [0,1).

    Uses {(G+n)/2, -(G-n)/2} with G = |n|/(1-kappa) >= |n|; net = n, gross = G.
    Demonstrates that kappa carries no decomposition-free information.
    """
    if not (0.0 <= target_kappa < 1.0):
        raise ValueError("target kappa must lie in [0,1)")
    if net == 0:
        raise ValueError("construction requires net != 0")
    G = abs(net) / (1.0 - target_kappa)
    return analyze(["hi", "lo"], [(G + net) / 2.0, -(G - net) / 2.0])


# ==========================================================================
# 3.  Marginal blindness -- two logically independent statements
# ==========================================================================
def decomposition_blindness(decomp: Decomposition, power: int = 2) -> dict:
    """f(net) cannot see gross or kappa.  Compare against a same-net singleton."""
    naive = analyze(["net_only"], [decomp.net])
    O_real, O_naive = decomp.net ** power, naive.net ** power
    return {
        "observable": f"O ~ net^{power}",
        "O(real decomposition)": O_real,
        "O(single same-net channel)": O_naive,
        "identical": bool(abs(O_real - O_naive) <= 1e-18 * max(1.0, abs(O_real))),
        "kappa_real": decomp.kappa,
        "kappa_naive": naive.kappa,
        "gross_real": decomp.gross,
        "gross_naive": naive.gross,
        "reading": "same observable, different cancellation structure: not distinguishable",
    }


def sign_blindness(decomp: Decomposition, power: int = 2) -> dict:
    """If the observable is EVEN in net it also cannot see sign(net).

    P_R ~ net^2 is even, so the amplitude reads |net|.  In Turok-Boyle this is
    not an artefact of bookkeeping: flipping sign(c_beta) flips R, but delta-chi
    is a zero-mean Gaussian field, so the sign does not enter the two-point
    function that defines P_R.
    """
    flipped = analyze([c + "(flipped)" for c in decomp.channels], -decomp.values)
    O, O_flip = decomp.net ** power, flipped.net ** power
    even = (power % 2 == 0)
    return {
        "observable": f"O ~ net^{power}",
        "even_in_net": even,
        "net": decomp.net,
        "net_flipped": flipped.net,
        "O(net)": O,
        "O(-net)": O_flip,
        "identical": bool(abs(O - O_flip) <= 1e-18 * max(1.0, abs(O))),
        "kappa_invariant_under_flip": bool(abs(decomp.kappa - flipped.kappa) < 1e-15),
        "reading": ("even observable reads |net| only" if even else
                    "odd observable does resolve the sign"),
    }


# ==========================================================================
# 4.  Turok-Boyle inputs (arXiv:2302.00344), computed rather than hardcoded
# ==========================================================================
# Eq. (4):  c_beta = (125/108) aY^2 - (95/72) a2^2 - (49/6) a3^2
TB_COEF = {"U(1)_Y": 125 / 108, "SU(2)_L": -95 / 72, "SU(3)_c": -49 / 6}

# Group data as quoted in TB Sec. III:  (C_A, S_F)
TB_GROUP = {"U(1)_Y": (0, 5), "SU(2)_L": (2, 3), "SU(3)_c": (3, 3)}

COUPLINGS = {
    # TB Sec. VII, from Buttazzo et al. (2013)
    "planck": {"U(1)_Y": 0.0181, "SU(2)_L": 0.0203, "SU(3)_c": 0.0189},
    # illustrative only: same high-T expression evaluated far below its natural
    # domain, to display the running.  The two orders of magnitude are the
    # point; the second digit is not.
    "electroweak": {"U(1)_Y": (1 / 128) / (1 - 0.231),
                    "SU(2)_L": (1 / 128) / 0.231,
                    "SU(3)_c": 0.1184},
}

REFERENCE = {                    # revised note, Tables 3 and 4
    "level1_net": -3.081766620e-3,
    "level1_gross": 3.840123102e-3,
    "level1_kappa": 0.19748234,
    "level2_gross": 8.479034769e-3,
    "level2_kappa": 0.63654275,
    "electroweak_kappa": 0.00206,
    "P_a": {"U(1)_Y": 25 / 144, "SU(2)_L": 19 / 48, "SU(3)_c": 7 / 6},
}


def beta_coefficient(name: str) -> float:
    """b_a = (11/3) C_A - (4/3) S_F, the one-loop combination."""
    C_A, S_F = TB_GROUP[name]
    return 11 / 3 * C_A - 4 / 3 * S_F


def level1(scale: str = "planck") -> Decomposition:
    """Level 1: the three gauge factors, from Eq. (4) at the given scale."""
    a = COUPLINGS[scale]
    names = list(TB_COEF)
    return analyze(names, [TB_COEF[n] * a[n] ** 2 for n in names])


def positive_factors(scale: str = "planck") -> dict:
    """P_a := -c_a / (alpha_a^2 b_a).  ALGEBRAIC for all three channels.

    The alpha^2 cancels, so each P_a is a pure rational number and does not
    run.  Turok and Boyle interpret this factor thermally (via <F^2>_T) for
    SU(3) ONLY.  Positivity is a computed fact; no thermal identification is claimed
    for U(1)_Y or SU(2)_L.  Nothing downstream depends on the interpretation --
    only on P_a > 0, which is what carries all the signs onto b_a.
    """
    # The alpha^2 cancels, so P_a is a pure rational number, independent of
    # scale: 25/144, 19/48, 7/6.  The `scale` argument is kept only so callers
    # can pass it uniformly alongside level1()/level2().
    del scale
    return {n: -TB_COEF[n] / beta_coefficient(n) for n in TB_COEF}


def level2(scale: str = "planck") -> Decomposition:
    """Level 2: split each b_a into antiscreening (11/3 C_A) and screening (4/3 S_F).

    This is the split TB write out as (11 - 2 n_f / 3) for SU(3).  Same net by
    construction; gross and kappa both rise.
    """
    a, P = COUPLINGS[scale], positive_factors(scale)
    lab, val = [], []
    for n, (C_A, S_F) in TB_GROUP.items():
        if C_A:                                    # U(1) has no gauge self-coupling
            lab.append(f"{n} gauge")
            val.append(-P[n] * a[n] ** 2 * (11 / 3 * C_A))
        lab.append(f"{n} matter")
        val.append(+P[n] * a[n] ** 2 * (4 / 3 * S_F))
    return analyze(lab, val)


def tilt(scale: str = "planck") -> float:
    """n_s - 1 = 2 beta_a3 / a3 = -b_3 alpha_3 / pi.

    TIER 2: this rests on the heuristic wavelength-to-running assumptions that
    Turok and Boyle explicitly flag as unverified.  Note it reads the
    COMBINATION b_3 * alpha_3, not b_3 alone, and is independent of P_SU(3).
    """
    return -beta_coefficient("SU(3)_c") * COUPLINGS[scale]["SU(3)_c"] / np.pi


# ==========================================================================
# 5.  Ensemble mode (Tier 3) -- varies the THEORY, not the resolution
# ==========================================================================
def ensemble(decomps: Sequence[Decomposition]) -> dict:
    """Spread of kappa across an ensemble at FIXED resolution.

    Scope note: resolution dependence is already settled formally by the
    monotonicity theorem, so this mode is only meaningful for comparing
    genuinely different theories (e.g. BSM completions) under one fixed
    decomposition scheme.  A single physical system cannot populate it, and
    clustering here would not make kappa an invariant.  Tier 3; certifies
    nothing.
    """
    ks = np.array([d.kappa for d in decomps if not np.isnan(d.kappa)], float)
    if ks.size == 0:
        return {"n": 0, "note": "no valid (nonzero-gross) decompositions"}
    nets = np.array([d.net for d in decomps], float)
    grosses = np.array([d.gross for d in decomps], float)
    mean = float(ks.mean())
    std = float(ks.std(ddof=1)) if ks.size > 1 else 0.0
    return {
        "n": int(ks.size),
        "kappa_mean": round(mean, 6),
        "kappa_std": round(std, 6),
        "kappa_cv": round(std / mean, 6) if mean > 0 else None,
        "net_range": (float(nets.min()), float(nets.max())),
        "gross_range": (float(grosses.min()), float(grosses.max())),
        "read": ("spread across theories at fixed resolution; says nothing about "
                 "resolution dependence, which Thm 6.2 settles formally"),
    }


# ==========================================================================
# 6.  Validation against the revised note
# ==========================================================================
def validate(verbose: bool = True) -> tuple[Decomposition, Decomposition]:
    def line(*a):
        if verbose:
            print(*a)

    def ok(x, y, tol):
        return "OK" if abs(x - y) <= tol else "??"

    line("=== VALIDATION against the revised note (Turok-Boyle, arXiv:2302.00344) ===")

    d1, d2 = level1("planck"), level2("planck")
    R = REFERENCE

    line("\n[1] Level 1 -- three gauge factors, from Eq. (4)")
    line(f"    net   = {d1.net:+.6e}  ref {R['level1_net']:+.6e}  "
         f"{ok(d1.net, R['level1_net'], 5e-9)}   (TB quote -0.0031)")
    line(f"    gross = {d1.gross:.6e}  ref {R['level1_gross']:.6e}  "
         f"{ok(d1.gross, R['level1_gross'], 5e-9)}")
    line(f"    kappa = {d1.kappa:.8f}    ref {R['level1_kappa']:.8f}       "
         f"{ok(d1.kappa, R['level1_kappa'], 5e-8)}")
    assert abs(d1.kappa - R["level1_kappa"]) < 5e-8

    line("\n[2] kappa identity  1-|net|/gross == 2*min(P,N)/gross")
    alt = 2.0 * min(d1.P, d1.N) / d1.gross
    line(f"    {d1.kappa:.12f} vs {alt:.12f}   {ok(d1.kappa, alt, 1e-12)}")
    assert abs(d1.kappa - alt) < 1e-12
    line(f"    (kappa is carried entirely by the single positive channel: "
         f"2*c_U(1)/gross = {2 * d1.P / d1.gross:.6f})")

    line("\n[3] Positive-factor / beta-coefficient decomposition (ALGEBRAIC)")
    P = positive_factors("planck")
    for n in TB_COEF:
        line(f"    {n:<9s} b_a = {beta_coefficient(n):+.4f}   P_a = {P[n]:.6f}   "
             f"ref {R['P_a'][n]:.6f}  {ok(P[n], R['P_a'][n], 1e-12)}   "
             f"P_a>0: {'OK' if P[n] > 0 else '??'}")
        assert P[n] > 0 and abs(P[n] - R["P_a"][n]) < 1e-12
    line("    NOTE: thermal reading of P_a is sourced for SU(3) only (TB Sec. VI).")

    line("\n[4] Level 2 -- gauge-boson / matter refinement")
    line(f"    net   = {d2.net:+.6e}  (unchanged: "
         f"{ok(d2.net, d1.net, 1e-15)})")
    line(f"    gross = {d2.gross:.6e}  ref {R['level2_gross']:.6e}  "
         f"{ok(d2.gross, R['level2_gross'], 5e-9)}")
    line(f"    kappa = {d2.kappa:.8f}    ref {R['level2_kappa']:.8f}       "
         f"{ok(d2.kappa, R['level2_kappa'], 5e-8)}")
    assert abs(d2.net - d1.net) < 1e-15
    assert d2.gross > d1.gross and d2.kappa > d1.kappa

    line("\n[5] Monotonicity (Thm 6.2 i-iii) on the level1 -> level2 step")
    groups = [[0], [1, 2], [3, 4]]           # U(1); SU(2) g+m; SU(3) g+m
    rep = refinement_report(d1, d2, groups)
    line(f"    net invariant        : {rep['net_invariant']}")
    line(f"    gross non-decreasing : {rep['gross_non_decreasing']}  "
         f"({rep['gross_parent']:.4e} -> {rep['gross_child']:.4e})")
    line(f"    kappa non-decreasing : {rep['kappa_non_decreasing']}  "
         f"({rep['kappa_parent']:.4f} -> {rep['kappa_child']:.4f})")
    line(f"    sign-homogeneous?    : {rep['sign_homogeneous']}   "
         f"equality holds? {rep['equality_holds']}   "
         f"consistent: {rep['equality_matches_homogeneity']}")
    assert rep["net_invariant"] and rep["kappa_non_decreasing"]
    assert rep["equality_matches_homogeneity"]

    line("\n[6] Thm 6.2(vi): refine c_r = (c_r + X, -X); threshold X > max(0,-c_r)")
    for row in kappa_span(list(d1.values), index=2):
        line(f"    X={row['X']:<8g} crosses={str(row['crosses_sign_boundary']):<5s} "
             f"kappa={row['kappa']:.6f}  unchanged={row['kappa_unchanged']}")
    rows = kappa_span(list(d1.values), index=2)
    assert rows[0]["kappa_unchanged"] and not rows[0]["crosses_sign_boundary"]
    assert rows[-1]["kappa"] > 0.99

    line("\n[7] kappa carries no decomposition-free information")
    for target in (0.0, 0.25, 0.5, 0.9):
        d = realize_kappa(d1.net, target)
        line(f"    target {target:.2f} -> realized {d.kappa:.6f}, net "
             f"{d.net:+.6e} {ok(d.net, d1.net, 1e-15)}")
        assert abs(d.kappa - target) < 1e-12 and abs(d.net - d1.net) < 1e-15

    line("\n[8] Two independent blindnesses of the amplitude (P_R ~ net^2)")
    db, sb = decomposition_blindness(d1), sign_blindness(d1)
    line(f"    decomposition: identical={db['identical']} across "
         f"kappa {db['kappa_real']:.4f} vs {db['kappa_naive']:.4f}")
    line(f"    sign         : identical={sb['identical']} for net "
         f"{sb['net']:+.4e} vs {sb['net_flipped']:+.4e}")
    line(f"    kappa itself is also flip-invariant: {sb['kappa_invariant_under_flip']}")
    line(f"    (an ODD observable would resolve the sign: "
         f"{not sign_blindness(d1, power=1)['identical']})")
    assert db["identical"] and sb["identical"]
    assert not sign_blindness(d1, power=1)["identical"]

    line("\n[9] Structural guard")
    line(f"    {classify_structure(d1.values)}")
    assert classify_structure(d1.values).startswith("signed L1")
    assert classify_structure([1.0, 2.0]).startswith("positive simplex")

    line("\n[10] Scale dependence (level 1)")
    for s in COUPLINGS:
        d = level1(s)
        line(f"    {s:<12s} net={d.net:+.4e}  kappa={d.kappa:.6f}")
    kew = level1("electroweak").kappa
    line(f"    ratio kappa(planck)/kappa(electroweak) = {d1.kappa / kew:.1f}")
    assert abs(kew - R["electroweak_kappa"]) < 5e-5

    line("\n[11] Edge cases")
    line(f"    net == 0  -> kappa = {net_gross_kappa([1.0, -1.0])[2]:.1f} "
         f"(total cancellation; kappa == 1, not < 1)")
    line(f"    gross == 0 -> kappa = {net_gross_kappa([0.0, 0.0])[2]} (undefined)")
    line(f"    zeros are sign-homogeneous: {is_sign_homogeneous([1.0, 0.0, 2.0])}")
    assert net_gross_kappa([1.0, -1.0])[2] == 1.0
    assert np.isnan(net_gross_kappa([0.0, 0.0])[2])

    line("\n[12] Tier 2 (heuristic, TB's own caveat): tilt")
    line(f"    n_s - 1 = -b_3*alpha_3/pi = {tilt():.6f}   (TB quote -0.042, "
         f"n_s = {1 + tilt():.4f})")
    line(f"    reads the COMBINATION b_3*alpha_3 = "
         f"{beta_coefficient('SU(3)_c') * COUPLINGS['planck']['SU(3)_c']:.4f}, not b_3 alone")

    line("\nAll assertions passed.")
    return d1, d2


# ==========================================================================
# 7.  CLI
# ==========================================================================
if __name__ == "__main__":
    import argparse
    import json

    ap = argparse.ArgumentParser(
        description="Signed Context Decomposition Analyzer (v2)")
    ap.add_argument("--validate", action="store_true",
                    help="reproduce the revised note's tables and theorem checks")
    ap.add_argument("--levels", action="store_true",
                    help="print both resolutions side by side")
    ap.add_argument("--scale", default="planck", choices=list(COUPLINGS),
                    help="renormalization scale for the built-in channels")
    ap.add_argument("--values", type=float, nargs="*",
                    help="analyze an arbitrary signed vector")
    ap.add_argument("--labels", type=str, nargs="*",
                    help="optional labels (must match --values length)")
    args = ap.parse_args()

    if args.values:
        labels = args.labels or [f"c{i}" for i in range(len(args.values))]
        d = analyze(labels, args.values)
        print(d.summary())
        print("\nstructure:", classify_structure(args.values))
        print("\nCAUTION: gross and kappa above describe THIS resolution only. "
              "Refining any channel across the sign boundary can only raise "
              "kappa (Thm 6.2), without limit.")
        print(json.dumps(decomposition_blindness(d), indent=2, default=str))
    elif args.levels:
        for name, d in (("LEVEL 1 (gauge factors)", level1(args.scale)),
                        ("LEVEL 2 (gauge/matter)", level2(args.scale))):
            print(f"=== {name} @ {args.scale} ===")
            print(d.summary())
            print()
        print("Same net by construction; gross and kappa are resolution-relative.")
    else:
        validate()

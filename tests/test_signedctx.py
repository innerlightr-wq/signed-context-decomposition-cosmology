"""Tests for the canonical ``signedctx`` implementation.

Every test imports the top-level ``signedctx`` module -- the same import a user
makes and the same one the README documents.  There is exactly one
implementation in the repository; see ``docs/CODE_ARCHITECTURE.md``.

The numerical values exercised here are *reproductions* of the repository's own
reference table, which in turn reproduces Turok-Boyle's inputs.  They are not
independent physical predictions; see ``docs/NOVELTY_AND_PROVENANCE.md``.
"""

import math

import numpy as np
import pytest

import signedctx
from signedctx import (
    COUPLINGS,
    REFERENCE,
    TB_COEF,
    TB_GROUP,
    analyze,
    beta_coefficient,
    classify_structure,
    coarsen,
    decomposition_blindness,
    ensemble,
    is_sign_homogeneous,
    kappa_span,
    level1,
    level2,
    net_gross_kappa,
    positive_factors,
    realize_kappa,
    refine,
    refinement_report,
    sign_blindness,
    sign_masses,
    tilt,
    validate,
)

PLANCK_CHANNELS = ["U(1)_Y", "SU(2)_L", "SU(3)_c"]


# --------------------------------------------------------------------------
# the import itself
# --------------------------------------------------------------------------


def test_the_imported_module_is_the_repository_root_module():
    """Guard against a second implementation shadowing the canonical one."""
    from pathlib import Path

    here = Path(__file__).resolve().parents[1]
    assert Path(signedctx.__file__).resolve() == (here / "signedctx.py").resolve()


def test_canonical_module_exposes_the_documented_api():
    for name in (
        "net_gross_kappa", "sign_masses", "analyze", "refine", "coarsen",
        "refinement_report", "kappa_span", "realize_kappa",
        "decomposition_blindness", "sign_blindness",
        "beta_coefficient", "level1", "level2", "positive_factors", "tilt",
        "ensemble", "validate", "classify_structure", "is_sign_homogeneous",
    ):
        assert hasattr(signedctx, name), f"missing public name: {name}"


# --------------------------------------------------------------------------
# basic signed-context identities
# --------------------------------------------------------------------------


def test_net_and_gross_are_plain_sums():
    values = [0.5, -0.25, 0.125]
    net, gross, _ = net_gross_kappa(values)
    assert net == pytest.approx(sum(values))
    assert gross == pytest.approx(sum(abs(v) for v in values))


def test_kappa_definition():
    values = [0.5, -0.25, 0.125]
    net, gross, kappa = net_gross_kappa(values)
    assert kappa == pytest.approx(1.0 - abs(net) / gross)


def test_kappa_agrees_with_the_sign_mass_form():
    """kappa == 2*min(P, N) / (P + N)."""
    for values in ([0.5, -0.25, 0.125], [1.0, -3.0], [2.0, -2.0], [7.0, -1.0, -1.0]):
        _, _, kappa = net_gross_kappa(values)
        P, N = sign_masses(values)
        assert kappa == pytest.approx(2.0 * min(P, N) / (P + N))


def test_sign_masses_recover_net_and_gross():
    values = [0.5, -0.25, 0.125]
    net, gross, _ = net_gross_kappa(values)
    P, N = sign_masses(values)
    assert P - N == pytest.approx(net)
    assert P + N == pytest.approx(gross)


def test_kappa_lies_in_the_unit_interval():
    rng = np.random.default_rng(20260918)
    for _ in range(200):
        values = rng.normal(size=rng.integers(1, 7))
        _, gross, kappa = net_gross_kappa(values)
        if gross > 0:
            assert 0.0 <= kappa <= 1.0


# --------------------------------------------------------------------------
# edge cases -- documented behaviour is preserved
# --------------------------------------------------------------------------


def test_all_positive_has_zero_cancellation():
    assert net_gross_kappa([1.0, 2.0, 3.0])[2] == pytest.approx(0.0)


def test_all_negative_has_zero_cancellation():
    assert net_gross_kappa([-1.0, -2.0, -3.0])[2] == pytest.approx(0.0)


def test_exact_cancellation_gives_kappa_one():
    net, gross, kappa = net_gross_kappa([2.5, -2.5])
    assert net == pytest.approx(0.0)
    assert gross == pytest.approx(5.0)
    assert kappa == pytest.approx(1.0)


def test_zero_vector_leaves_kappa_undefined_as_nan():
    """gross == 0: documented behaviour is nan, not 0 and not an exception."""
    net, gross, kappa = net_gross_kappa([0.0, 0.0])
    assert net == 0.0 and gross == 0.0
    assert math.isnan(kappa)


def test_single_channel_has_zero_cancellation():
    assert net_gross_kappa([5.0])[2] == pytest.approx(0.0)
    assert net_gross_kappa([-5.0])[2] == pytest.approx(0.0)


def test_two_channels_span_the_range():
    assert net_gross_kappa([1.0, 1.0])[2] == pytest.approx(0.0)
    assert net_gross_kappa([1.0, -1.0])[2] == pytest.approx(1.0)


def test_near_cancellation_approaches_one():
    _, _, kappa = net_gross_kappa([1.0, -(1.0 - 1e-9)])
    assert kappa > 1.0 - 1e-8


def test_analyze_reports_dominant_channel_and_signs():
    d = analyze(PLANCK_CHANNELS, [+3.8e-4, -5.4e-4, -2.9e-3])
    assert d.dom_ch == "SU(3)_c"
    assert d.signs == ("+", "-", "-")
    assert d.dom_frac == pytest.approx(2.9e-3 / d.gross)


def test_analyze_rejects_length_mismatch():
    with pytest.raises(ValueError):
        analyze(["a", "b"], [1.0])


def test_classify_structure_separates_signed_from_positive():
    assert "signed" in classify_structure([1.0, -1.0]).lower()
    assert "simplex" in classify_structure([1.0, 2.0]).lower()


def test_is_sign_homogeneous_ignores_zeros():
    assert is_sign_homogeneous([1.0, 0.0, 2.0])
    assert is_sign_homogeneous([-1.0, 0.0, -2.0])
    assert not is_sign_homogeneous([1.0, -2.0])


# --------------------------------------------------------------------------
# refine / coarsen / refinement invariants
# --------------------------------------------------------------------------


def test_refine_requires_pieces_to_sum_to_the_parent():
    with pytest.raises(ValueError):
        refine(["a", "b"], [3.0, -1.0], 0, [1.0, 1.0])  # sums to 2, not 3


def test_refine_preserves_net_exactly():
    parent = analyze(["a", "b"], [3.0, -1.0])
    child = refine(["a", "b"], [3.0, -1.0], 0, [1.0, 2.0])
    assert child.net == pytest.approx(parent.net)


def test_sign_homogeneous_refinement_preserves_gross_and_kappa():
    """Exact rational example: split +3 into +1, +2."""
    parent = analyze(["a", "b"], [3.0, -1.0])
    child = refine(["a", "b"], [3.0, -1.0], 0, [1.0, 2.0])
    assert is_sign_homogeneous([1.0, 2.0])
    assert child.gross == pytest.approx(parent.gross)
    assert child.kappa == pytest.approx(parent.kappa)


def test_sign_crossing_refinement_increases_gross_and_kappa():
    """Split +3 into +4, -1: gross 4 -> 6, kappa 0.5 -> 2/3."""
    parent = analyze(["a", "b"], [3.0, -1.0])
    child = refine(["a", "b"], [3.0, -1.0], 0, [4.0, -1.0])
    assert parent.gross == pytest.approx(4.0)
    assert parent.kappa == pytest.approx(0.5)
    assert child.gross == pytest.approx(6.0)
    assert child.kappa == pytest.approx(2.0 / 3.0)
    assert child.net == pytest.approx(parent.net)
    assert child.gross > parent.gross
    assert child.kappa > parent.kappa


def test_coarsen_inverts_a_refinement():
    child = refine(["a", "b"], [3.0, -1.0], 0, [4.0, -1.0])
    back = coarsen(list(child.channels), list(child.values), [[0, 1], [2]])
    assert back.net == pytest.approx(3.0 - 1.0)
    assert back.gross == pytest.approx(4.0)
    assert back.kappa == pytest.approx(0.5)


def test_coarsen_rejects_a_non_partition():
    with pytest.raises(ValueError):
        coarsen(["a", "b", "c"], [1.0, 2.0, 3.0], [[0, 1]])


def test_refinement_report_flags_the_three_properties():
    parent = analyze(["a", "b"], [3.0, -1.0])
    child = refine(["a", "b"], [3.0, -1.0], 0, [4.0, -1.0])
    rep = refinement_report(parent, child, groups=[[0, 1], [2]])
    assert rep["net_invariant"] is True
    assert rep["gross_non_decreasing"] is True
    assert rep["kappa_non_decreasing"] is True
    assert rep["sign_homogeneous"] is False


def test_kappa_span_is_monotone_in_the_crossing_amount():
    rows = kappa_span([3.0, -1.0], index=0, Xs=(1e-3, 1e-2, 1e0, 1e3))
    kappas = [r["kappa"] for r in rows]
    assert kappas == sorted(kappas)
    assert kappas[-1] > 0.99


# --------------------------------------------------------------------------
# realize_kappa
# --------------------------------------------------------------------------


@pytest.mark.parametrize("target", [0.0, 0.1, 0.5, 0.9, 0.99])
@pytest.mark.parametrize("net", [1.0, -2.5, -3.081766620370e-03])
def test_realize_kappa_hits_the_target_at_fixed_net(net, target):
    d = realize_kappa(net, target)
    assert d.net == pytest.approx(net, rel=1e-12, abs=1e-15)
    assert d.kappa == pytest.approx(target, abs=1e-12)
    assert len(d.values) == 2
    assert d.net == pytest.approx(float(np.sum(d.values)))
    assert d.gross == pytest.approx(float(np.sum(np.abs(d.values))))


def test_realize_kappa_zero_target_is_sign_homogeneous():
    d = realize_kappa(-3.0, 0.0)
    assert d.kappa == pytest.approx(0.0)
    assert is_sign_homogeneous(list(d.values))


def test_realize_kappa_rejects_targets_outside_the_half_open_unit_interval():
    for bad in (-0.1, 1.0, 1.5):
        with pytest.raises(ValueError):
            realize_kappa(1.0, bad)


def test_realize_kappa_rejects_zero_net():
    with pytest.raises(ValueError):
        realize_kappa(0.0, 0.5)


# --------------------------------------------------------------------------
# level1 / level2 -- reproduction of the repository reference table
# --------------------------------------------------------------------------


def test_beta_coefficients_follow_from_the_group_data():
    """b_a = (11/3) C_A - (4/3) S_F on the (C_A, S_F) pairs quoted by Turok-Boyle."""
    for ch, (C_A, S_F) in TB_GROUP.items():
        assert beta_coefficient(ch) == pytest.approx((11.0 / 3.0) * C_A - (4.0 / 3.0) * S_F)
    assert beta_coefficient("U(1)_Y") == pytest.approx(-20.0 / 3.0)
    assert beta_coefficient("SU(2)_L") == pytest.approx(10.0 / 3.0)
    assert beta_coefficient("SU(3)_c") == pytest.approx(7.0)


def test_level1_reproduces_the_reference_table():
    d = level1("planck")
    assert list(d.channels) == PLANCK_CHANNELS
    assert d.net == pytest.approx(REFERENCE["level1_net"], rel=1e-9)
    assert d.gross == pytest.approx(REFERENCE["level1_gross"], rel=1e-9)
    assert d.kappa == pytest.approx(REFERENCE["level1_kappa"], rel=1e-7)
    assert d.signs == ("+", "-", "-")
    assert d.dom_ch == "SU(3)_c"


def test_level1_channels_are_c_a_equals_coefficient_times_alpha_squared():
    d = level1("planck")
    alphas = COUPLINGS["planck"]
    for ch, value in zip(d.channels, d.values):
        assert value == pytest.approx(TB_COEF[ch] * alphas[ch] ** 2, rel=1e-12)


def test_level1_kappa_is_carried_by_the_single_positive_channel():
    d = level1("planck")
    P, _ = sign_masses(list(d.values))
    assert d.kappa == pytest.approx(2.0 * P / d.gross, rel=1e-12)


def test_positive_factors_are_the_reference_rationals_and_do_not_run():
    at_planck = positive_factors("planck")
    at_ew = positive_factors("electroweak")
    for ch, expected in REFERENCE["P_a"].items():
        assert at_planck[ch] == pytest.approx(expected, rel=1e-12)
        assert at_ew[ch] == pytest.approx(expected, rel=1e-12)


def test_level2_reproduces_the_reference_table():
    d = level2("planck")
    assert len(d.values) == 5
    assert d.net == pytest.approx(REFERENCE["level1_net"], rel=1e-9)
    assert d.gross == pytest.approx(REFERENCE["level2_gross"], rel=1e-9)
    assert d.kappa == pytest.approx(REFERENCE["level2_kappa"], rel=1e-7)


def test_level1_to_level2_preserves_net_and_raises_gross_and_kappa():
    d1, d2 = level1("planck"), level2("planck")
    assert d2.net == pytest.approx(d1.net, rel=1e-12)
    assert d2.gross > d1.gross
    assert d2.kappa > d1.kappa
    rep = refinement_report(d1, d2, groups=[[0], [1, 2], [3, 4]])
    assert rep["net_invariant"] is True
    assert rep["gross_non_decreasing"] is True
    assert rep["kappa_non_decreasing"] is True
    assert rep["sign_homogeneous"] is False


def test_electroweak_kappa_is_two_orders_of_magnitude_smaller():
    k_planck = level1("planck").kappa
    k_ew = level1("electroweak").kappa
    assert k_ew == pytest.approx(REFERENCE["electroweak_kappa"], abs=1e-5)
    assert k_planck / k_ew > 50.0


def test_unknown_scale_is_rejected():
    with pytest.raises((KeyError, ValueError)):
        level1("no_such_scale")


# --------------------------------------------------------------------------
# tilt -- reproduction of the Turok-Boyle approximation, not a prediction
# --------------------------------------------------------------------------


def test_tilt_reproduces_the_turok_boyle_approximation():
    """n_s - 1 = -b_3 * alpha_3 / pi.

    This reproduces the heuristic tilt relation of Turok-Boyle (arXiv:2302.00344,
    Eq. 16), who describe that analysis as resting on assumptions they have not
    verified.  It is a reproduction of their approximation, NOT an independent
    physical prediction by this repository.
    """
    value = tilt("planck")
    b3 = beta_coefficient("SU(3)_c")
    a3 = COUPLINGS["planck"]["SU(3)_c"]
    assert value == pytest.approx(-b3 * a3 / math.pi, rel=1e-12)
    assert value == pytest.approx(-0.042, abs=5e-4)
    assert 1.0 + value == pytest.approx(0.9579, abs=1e-3)


def test_tilt_reads_only_the_su3_channel():
    """It is independent of P_3 and of the other two gauge factors."""
    assert tilt("planck") != pytest.approx(tilt("electroweak"))
    b3 = beta_coefficient("SU(3)_c")
    for scale in ("planck", "electroweak"):
        a3 = COUPLINGS[scale]["SU(3)_c"]
        assert tilt(scale) == pytest.approx(-b3 * a3 / math.pi, rel=1e-12)


# --------------------------------------------------------------------------
# the two blindnesses
# --------------------------------------------------------------------------


def test_even_observable_is_blind_to_the_decomposition():
    d = level1("planck")
    rep = decomposition_blindness(d, power=2)
    assert rep["identical"] is True
    assert rep["kappa_real"] == pytest.approx(d.kappa)
    assert rep["kappa_naive"] == pytest.approx(0.0)


def test_even_observable_is_also_blind_to_the_sign():
    d = level1("planck")
    rep = sign_blindness(d, power=2)
    assert rep["identical"] is True
    assert rep["kappa_invariant_under_flip"] is True


def test_odd_observable_resolves_the_sign():
    d = level1("planck")
    assert sign_blindness(d, power=1)["identical"] is False


def test_blindness_holds_for_every_even_power():
    d = analyze(["a", "b", "c"], [0.5, -0.25, 0.125])
    for power in (2, 4, 6):
        assert decomposition_blindness(d, power=power)["identical"] is True


def test_ensemble_reports_zero_spread_for_identical_members():
    d = level1("planck")
    stats = ensemble([d, d, d])
    assert stats["n"] == 3
    # ``ensemble`` rounds its summary statistics for display (6 decimals), so the
    # tolerance here matches that rounding rather than full precision.
    assert stats["kappa_mean"] == pytest.approx(d.kappa, abs=1e-6)
    assert stats["kappa_std"] == pytest.approx(0.0)
    assert stats["net_range"][0] == pytest.approx(stats["net_range"][1])
    assert stats["gross_range"][0] == pytest.approx(stats["gross_range"][1])


def test_ensemble_reports_positive_spread_for_differing_members():
    a, b = level1("planck"), level1("electroweak")
    stats = ensemble([a, b])
    assert stats["n"] == 2
    assert stats["kappa_std"] > 0.0


# --------------------------------------------------------------------------
# the module's own self-check
# --------------------------------------------------------------------------


def test_module_self_check_passes():
    """``python signedctx.py`` asserts the whole reference table; run it here too."""
    validate()

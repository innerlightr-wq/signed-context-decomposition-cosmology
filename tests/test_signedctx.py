"""Unit tests for the signed context decomposition analyzer.

Coverage is deliberately modest: the exact invariants, the algebraic identity
between the two forms of kappa, the structural guard, marginal-blindness, the
ensemble diagnostic, and the paper's Table 1.
"""

import math

import numpy as np
import pytest

from signedctx import (
    POSITIVE_SIMPLEX,
    SIGNED_L1,
    TRACE_ANOMALY,
    amplitude_blindness,
    classify_structure,
    decompose,
    ensemble_kappa_statistics,
    net_gross_kappa,
    positive_negative_masses,
    validate_against_paper,
)

# A few representative signed contexts used across the property tests.
SAMPLE_CONTEXTS = [
    [1.0, 2.0, 3.0],
    [-1.0, -2.0, -3.0],
    [1.0, -1.0, 2.0],
    [10.0, -9.9],
    [0.5, -0.3, 0.2],
    [+0.00038, -0.00054, -0.00292],
    [7.0],
    [0.0, 3.0, -1.0],
]


# --- core invariants -------------------------------------------------------
def test_net_and_gross_are_plain_sums():
    net, gross, _ = net_gross_kappa([1.0, -2.0, 4.0])
    assert net == pytest.approx(3.0)
    assert gross == pytest.approx(7.0)


@pytest.mark.parametrize("values", SAMPLE_CONTEXTS)
def test_kappa_identity_agrees_with_sign_masses(values):
    """1 - |net|/gross must equal 2*min(P, N)/gross exactly."""
    _, gross, kappa = net_gross_kappa(values)
    positive_mass, negative_mass = positive_negative_masses(values)
    assert kappa == pytest.approx(
        2.0 * min(positive_mass, negative_mass) / gross, abs=1e-12
    )


@pytest.mark.parametrize("values", SAMPLE_CONTEXTS)
def test_kappa_lies_in_unit_interval(values):
    _, _, kappa = net_gross_kappa(values)
    assert 0.0 <= kappa < 1.0


@pytest.mark.parametrize("values", SAMPLE_CONTEXTS)
def test_masses_recover_net_and_gross(values):
    net, gross, _ = net_gross_kappa(values)
    positive_mass, negative_mass = positive_negative_masses(values)
    assert positive_mass - negative_mass == pytest.approx(net)
    assert positive_mass + negative_mass == pytest.approx(gross)


def test_same_sign_context_has_zero_cancellation():
    _, _, kappa = net_gross_kappa([2.0, 3.0, 5.0])
    assert kappa == pytest.approx(0.0)


def test_exact_cancellation_gives_kappa_one():
    net, gross, kappa = net_gross_kappa([1.0, -1.0])
    assert net == pytest.approx(0.0)
    assert gross == pytest.approx(2.0)
    assert kappa == pytest.approx(1.0)


def test_all_zero_context_leaves_kappa_undefined():
    net, gross, kappa = net_gross_kappa([0.0, 0.0])
    assert (net, gross) == (0.0, 0.0)
    assert math.isnan(kappa)


# --- decompose() -----------------------------------------------------------
def test_decompose_reports_dominant_channel_and_signs():
    context = decompose(["a", "b", "c"], [1.0, -1.0, 2.0])
    assert context.dominant_channel == "c"
    assert context.dominant_fraction == pytest.approx(0.5)
    assert context.signs == ("+", "-", "+")
    assert context.structure == SIGNED_L1


def test_decompose_rejects_length_mismatch():
    with pytest.raises(ValueError):
        decompose(["a", "b"], [1.0])


def test_decompose_rejects_empty_context():
    with pytest.raises(ValueError):
        decompose([], [])


def test_as_dict_is_json_friendly():
    payload = decompose(["a", "b"], [1.0, -2.0]).as_dict()
    assert payload["net"] == pytest.approx(-1.0)
    assert payload["channels"] == ["a", "b"]
    assert all(isinstance(value, float) for value in payload["values"])


def test_summary_mentions_the_invariants():
    text = decompose(["a", "b"], [1.0, -2.0]).summary()
    for expected in ("net", "gross", "kappa", "dominant", "structure"):
        assert expected in text


# --- structural guard ------------------------------------------------------
def test_non_negative_context_is_a_positive_simplex():
    assert classify_structure([0.5, 0.3, 0.0]) == POSITIVE_SIMPLEX


def test_mixed_sign_context_is_signed_l1():
    assert classify_structure([0.5, -0.3, 0.2]) == SIGNED_L1


# --- marginal-blindness ----------------------------------------------------
def test_amplitude_cannot_distinguish_contexts_with_equal_net():
    resolved = decompose(["big_plus", "big_minus"], [10.0, -9.9])
    report = amplitude_blindness(resolved, power=2)
    assert report["observables_identical"]
    assert report["observable_resolved"] == pytest.approx(0.1**2)
    # The observable is identical, but the cancellation structure is not.
    assert report["kappa_resolved"] > 0.9
    assert report["kappa_single_channel"] == pytest.approx(0.0)
    assert report["gross_resolved"] > report["gross_single_channel"]


@pytest.mark.parametrize("power", [1, 2, 3])
def test_blindness_holds_for_any_power(power):
    resolved = decompose(["a", "b", "c"], [3.0, -2.5, 0.25])
    assert amplitude_blindness(resolved, power=power)["observables_identical"]


# --- ensemble diagnostic ---------------------------------------------------
def test_ensemble_reports_zero_spread_for_identical_contexts():
    contexts = [decompose(["a", "b"], [1.0, -0.5]) for _ in range(3)]
    statistics = ensemble_kappa_statistics(contexts)
    assert statistics["n"] == 3
    assert statistics["kappa_std"] == pytest.approx(0.0)
    assert statistics["kappa_cv"] == pytest.approx(0.0)


def test_ensemble_handles_single_member():
    statistics = ensemble_kappa_statistics([decompose(["a", "b"], [1.0, -0.5])])
    assert statistics["n"] == 1
    assert statistics["kappa_std"] == pytest.approx(0.0)


def test_ensemble_skips_undefined_kappa():
    statistics = ensemble_kappa_statistics([decompose(["a"], [0.0])])
    assert statistics["n"] == 0
    assert "note" in statistics


# --- the paper's Table 1 ---------------------------------------------------
def test_table_1_is_reproduced():
    context = decompose(TRACE_ANOMALY["channels"], TRACE_ANOMALY["values"])
    assert context.net == pytest.approx(TRACE_ANOMALY["paper_net"], abs=5e-6)
    assert context.gross == pytest.approx(TRACE_ANOMALY["paper_gross"], abs=5e-6)
    assert context.kappa == pytest.approx(TRACE_ANOMALY["paper_kappa"], abs=5e-3)
    assert context.dominant_channel == "SU(3)_c"
    assert context.structure == SIGNED_L1


def test_validate_against_paper_runs_quietly():
    context = validate_against_paper(verbose=False)
    assert isinstance(context.values, np.ndarray)
    assert context.kappa == pytest.approx(0.1979, abs=1e-4)

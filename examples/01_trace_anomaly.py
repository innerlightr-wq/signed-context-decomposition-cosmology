"""Example 1 -- reproduce Table 1 of the paper.

The three Planck-scale gauge contributions to the trace-anomaly coefficient
c_beta are entered as a signed context; the exact invariants (net, gross,
kappa) are printed and compared with the reported values.

Run with:  python examples/01_trace_anomaly.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from signedctx import TRACE_ANOMALY, decompose, validate_against_paper  # noqa: E402

# Analyze the signed gauge-sector context directly.
gauge_context = decompose(TRACE_ANOMALY["channels"], TRACE_ANOMALY["values"])
print(gauge_context.summary())
print()

# About a fifth of the gross gauge magnitude cancels in the net.
print(f"cancellation index kappa = {gauge_context.kappa:.4f}")
print(f"paper value              = {TRACE_ANOMALY['paper_kappa']:.2f}")
print()

# The same numbers, plus the internal consistency checks.
validate_against_paper()

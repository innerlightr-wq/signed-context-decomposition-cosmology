"""Example 2 -- a net-only observable is blind to gross and kappa.

Two very different contexts are built with the *same* net value: one with
large sign-opposed channels that nearly cancel, one with a single channel.
An observable of the form O ~ net**2 (the scalar amplitude) returns the same
number for both, while gross and kappa differ sharply.

Run with:  python examples/02_marginal_blindness.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from signedctx import amplitude_blindness, decompose  # noqa: E402

# Two sizeable, sign-opposed channels leaving a small remainder.
near_cancelling = decompose(["big_plus", "big_minus"], [+10.0, -9.9])

# One small channel carrying the same net.
single_channel = decompose(["only"], [+0.1])

contexts = (("near-cancelling", near_cancelling), ("single channel", single_channel))
for label, context in contexts:
    print(f"{label:>16s}:  net = {context.net:+.4f}   "
          f"gross = {context.gross:7.4f}   kappa = {context.kappa:.4f}")
print()

# The amplitude sees only the net, so it cannot tell the two apart.
report = amplitude_blindness(near_cancelling, power=2)
print(f"O(near-cancelling context) = {report['observable_resolved']:.8g}")
print(f"O(same-net single channel) = {report['observable_single_channel']:.8g}")
print(f"identical: {report['observables_identical']}")
print()
print(report["reading"])

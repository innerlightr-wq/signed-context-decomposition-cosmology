"""Example 2 -- a net-only observable is blind to gross and kappa.

Two very different contexts are built with the *same* net: one with large
sign-opposed channels that nearly cancel, one with a single channel.  An
observable of the form O ~ net**2 (the scalar amplitude) returns the same number
for both, while gross and kappa differ sharply.  An *odd* observable resolves the
sign but still not the decomposition.

Both contexts here are algebraic witnesses, not physically realizable Standard
Model decompositions.

Run with:  python examples/02_marginal_blindness.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from signedctx import analyze, decomposition_blindness, sign_blindness  # noqa: E402

near_cancelling = analyze(["big_plus", "big_minus"], [+10.0, -9.9])
single_channel = analyze(["only"], [+0.1])

for label, context in (("near-cancelling", near_cancelling),
                       ("single channel", single_channel)):
    print(f"{label:>16s}:  net = {context.net:+.4f}   "
          f"gross = {context.gross:7.4f}   kappa = {context.kappa:.4f}")
print()

report = decomposition_blindness(near_cancelling, power=2)
print(f"observable                 : {report['observable']}")
print(f"O(near-cancelling context) = {report['O(real decomposition)']:.8g}")
print(f"O(same-net single channel) = {report['O(single same-net channel)']:.8g}")
print(f"identical                  : {report['identical']}")
print(f"kappa  resolved / naive    : {report['kappa_real']:.4f} / {report['kappa_naive']:.4f}")
print()
print(report["reading"])
print()

flip = sign_blindness(near_cancelling, power=2)
print(f"even observable is also sign-blind : {flip['identical']}")
print(f"kappa invariant under a sign flip  : {flip['kappa_invariant_under_flip']}")
print(f"an ODD observable resolves the sign: "
      f"{not sign_blindness(near_cancelling, power=1)['identical']}")

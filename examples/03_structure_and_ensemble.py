"""Example 3 -- the structural guard, and the ensemble diagnostic.

Part A shows that an all-positive context is classified as a positive simplex
(where a Fisher-geometric reading would apply after normalization) while a
mixed-sign context is classified as a signed L1 structure (where it does not).

Part B runs the ensemble diagnostic on a set of *hypothetical* decompositions.
It certifies nothing: a single physical system cannot populate such an ensemble,
and the values below are illustrative placeholders, not predictions.

Run with:  python examples/03_structure_and_ensemble.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from signedctx import analyze, classify_structure, ensemble  # noqa: E402

# --- Part A: positive simplex vs signed L1 --------------------------------
positive = [0.5, 0.3, 0.2]
signed = [0.5, -0.3, 0.2]

for label, values in (("all positive", positive), ("mixed sign", signed)):
    print(f"{label:>13s} -> {classify_structure(values)}")
print()

# --- Part B: does kappa cluster or spread? (illustrative only) ------------
hypothetical_completions = [
    analyze(["U(1)", "SU(2)", "SU(3)"], values)
    for values in (
        [+0.00038, -0.00054, -0.00292],
        [+0.00041, -0.00050, -0.00280],
        [+0.00035, -0.00061, -0.00301],
        [+0.00044, -0.00047, -0.00275],
    )
]

statistics = ensemble(hypothetical_completions)
for key in ("n", "kappa_mean", "kappa_std", "kappa_cv"):
    print(f"{key:>10s} = {statistics[key]}")
print()
print(statistics["read"])

"""Example 1 -- reproduce the repository's reference decomposition.

The three Planck-scale gauge contributions to the trace-anomaly coefficient
c_beta are computed from the coefficients and couplings in ``signedctx``, and the
descriptors (net, gross, kappa) are printed at both resolutions.

The numbers reproduce inputs imported from Turok-Boyle (and behind them
Arnold-Zhai and Buttazzo et al.); they are not independent predictions.  See
``docs/NOVELTY_AND_PROVENANCE.md``.

Run with:  python examples/01_trace_anomaly.py
"""

import sys
from pathlib import Path

# Put the repository root -- which holds the canonical ``signedctx.py`` -- on the
# path so this script runs from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from signedctx import REFERENCE, level1, level2, validate  # noqa: E402

level_1 = level1("planck")
print("Level 1 -- three gauge factors")
print(level_1.summary())
print()

level_2 = level2("planck")
print("Level 2 -- gauge-boson / matter refinement")
print(level_2.summary())
print()

print(f"net is preserved by the refinement: "
      f"{abs(level_2.net - level_1.net) < 1e-15}")
print(f"kappa rises {level_1.kappa:.6f} -> {level_2.kappa:.6f} "
      f"(the refinement crosses signs)")
print(f"reference kappa at level 1  = {REFERENCE['level1_kappa']}")
print()

# The module's own self-check: reproduces the whole reference table and asserts it.
validate()

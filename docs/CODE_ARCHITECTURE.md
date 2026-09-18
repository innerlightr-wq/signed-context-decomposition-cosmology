# Code architecture

**Canonical implementation:** `signedctx.py`, at the repository root. There is exactly one.

**Public import:** `import signedctx` — the same statement for users, tests, examples and the
README. No installation step is required; NumPy is the only runtime dependency.

| context | how it imports | resolves to |
|---|---|---|
| a user, from the repository root | `import signedctx` | `signedctx.py` |
| `pytest` (any working directory) | `import signedctx` | `signedctx.py` |
| `examples/*.py` | one-line insert of the repository root onto `sys.path` | `signedctx.py` |
| `python signedctx.py` | runs the module's own `--validate` self-check | `signedctx.py` |

`conftest.py` at the repository root exists **only** so that the import does not depend on the
current working directory: pytest prepends the directory containing the topmost `conftest.py` to
`sys.path`. It contains no code. Without it, `pytest` succeeds from the repository root (because
`python -m pytest` happens to put the working directory on the path) and fails with
`ModuleNotFoundError` from anywhere else — exactly the kind of accidental path dependence this
layout is meant to remove.

The examples insert the repository root because `python examples/01_trace_anomaly.py` puts
`examples/` on `sys.path`, not the root, and the filenames begin with digits so they cannot be run
as `-m` modules. That single line is a script idiom, not a workaround for a packaging problem.

## Why a second implementation was removed

Until this change the repository shipped **two** implementations:

* `signedctx.py` (root) — the version accompanying the current manuscript, with the full API:
  `level1`, `level2`, `refine`, `coarsen`, `refinement_report`, `kappa_span`, `realize_kappa`,
  `sign_blindness`, `tilt`, `beta_coefficient`, `positive_factors`, `validate`;
* `src/signedctx.py` — an older version for the **superseded** manuscript, which had none of those.

`tests/conftest.py` prepended `src/` to `sys.path`, and all three examples did the same. So the
identical statement `import signedctx` resolved to **different files** depending on context: the
modern module interactively, the stale one under `pytest`. The suite reported 44 passing tests
while never executing the code the README documents.

The two were compared function by function before removal. Findings:

* every name unique to `src/` was a **rename** of a canonical function — `decompose` → `analyze`,
  `positive_negative_masses` → `sign_masses`, `amplitude_blindness` →
  `decomposition_blindness`/`sign_blindness`, `ensemble_kappa_statistics` → `ensemble`,
  `validate_against_paper` → `validate`, `ZERO_GROSS_TOLERANCE` → `EPS`, and the
  `POSITIVE_SIMPLEX`/`SIGNED_L1`/`STRUCTURE_NOTES` tokens → prose returned by
  `classify_structure`. **No functionality existed only in `src/`.**
* the one substantive shared function, `net_gross_kappa`, returned **identical** values on every
  probe, including the documented `gross = 0 → nan` edge case;
* `src/` stored the channel values as hard-coded 2–3 significant-figure **roundings**
  (`[+0.00038, -0.00054, -0.00292]`, `paper_kappa = 0.2`), whereas the canonical module derives
  them from the exact coefficients and couplings. That accounts for a 0.22% relative difference in
  `kappa` (0.1979 vs 0.19748234) — a difference in **input precision, not in algebra**. The stale
  test asserted `kappa ≈ 0.2` with `abs=5e-3`, a tolerance too loose to notice.

So no mathematics, no physics and no published number changed when `src/signedctx.py` was deleted.
The self-check output of `python signedctx.py` is byte-identical before and after.

## Running everything

```bash
pip install -r requirements.txt     # numpy (runtime), pytest (tests)

python signedctx.py                 # self-check against the reference table
python signedctx.py --levels        # both resolutions side by side
pytest -q                           # the test suite

python examples/01_trace_anomaly.py
python examples/02_marginal_blindness.py
python examples/03_structure_and_ensemble.py
```

All of these work from any working directory.

## What the tests cover

`tests/test_signedctx.py` exercises the canonical module directly, including a guard
(`test_the_imported_module_is_the_repository_root_module`) that fails if a second implementation
ever shadows it again. Coverage includes the `net`/`gross`/`kappa` identities and the
`2 min(P,N)/(P+N)` form; the edge cases (all-positive, all-negative, exact cancellation, zero
vector → `nan`, one channel, two channels, near cancellation); `refine`/`coarsen` and the three
refinement properties on exact rational examples; `kappa_span`; `realize_kappa` across five targets
and three nets; `level1`/`level2` against the reference table with net preserved between levels;
`beta_coefficient` against the group data; `positive_factors`; `tilt`; both blindnesses; and the
module's own `validate()`.

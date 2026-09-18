# Manuscript

The manuscript is archived on Zenodo and is **not** committed to this repository.

- **Current revision accompanying this repository (cite this):**
  <https://doi.org/10.5281/zenodo.21780964>

Full reference:

> De Jesús, Elias (2026). *Two Blind Observables on a Signed Gauge Decomposition: An
> Invariance-Audited Diagnostic Reading of the Turok–Boyle Primordial Spectrum.* Technical Note.
> Zenodo. https://doi.org/10.5281/zenodo.21780964

- **Superseded earlier version** (different title, do not cite for the current content):
  <https://doi.org/10.5281/zenodo.20701311> — *Amplitude–Tilt Complementarity and the Gauge Trace
  Anomaly as a Signed Context Decomposition: A Partition-Diagnostic Reading of the Turok–Boyle
  Primordial Spectrum.*

The numerical inputs are reproduced by `signedctx.py` at the repository root, which is the single
canonical implementation; see [`../docs/CODE_ARCHITECTURE.md`](../docs/CODE_ARCHITECTURE.md).

## Provenance of the physical inputs

The Standard Model couplings and the trace-anomaly coefficient are **not** derived here. The chain is

    this repository
        <- N. Turok and L. Boyle, "A Minimal Explanation of the Primordial Cosmological
           Perturbations", arXiv:2302.00344 [hep-ph] (2023), Eq. (4)
              <- P. B. Arnold and C. X. Zhai, Phys. Rev. D 51 (1995) 1906, Eq. (5.1)
                 -- the trace-anomaly coefficient itself
              <- D. Buttazzo et al., JHEP 12 (2013) 089
                 -- the Planck-scale gauge couplings

See [`../docs/NOVELTY_AND_PROVENANCE.md`](../docs/NOVELTY_AND_PROVENANCE.md) for the full
input-to-use table and [`../docs/LITERATURE_CONTEXT.md`](../docs/LITERATURE_CONTEXT.md) for the
provenance discussion.

If you later prefer to ship the PDF with the code, place it here as `manuscript.pdf` and update the
repository organization section of the top-level `README.md`.

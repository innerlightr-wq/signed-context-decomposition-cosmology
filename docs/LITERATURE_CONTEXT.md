# Literature context

Organized by **where each part of this repository comes from**, not chronologically. Per-claim
provenance is in [`NOVELTY_AND_PROVENANCE.md`](NOVELTY_AND_PROVENANCE.md); verified records are in
[`../references.bib`](../references.bib) (22 entries, all with DOIs, every one obtained from
publisher or registry metadata).

**Scope rule.** Only sources that bear on a claim made here. Nothing is listed merely because it
was read.

---

## 1. The imported physics, and the chain behind it

The repository computes with one physical input: the high-temperature Standard Model
trace-anomaly coefficient. The provenance chain has **three** links, and the repository currently
cites only the first.

    this repository
        <- Turok & Boyle (2023), Eq. (4)                    [TB23]
              <- Arnold & Zhai (1995), Eq. (5.1)            [AZ95]   the coefficient itself
              <- Buttazzo et al. (2013), via TB's Ref. [37] [Bu13]   the Planck-scale couplings

**[TB23]** *A Minimal Explanation of the Primordial Cosmological Perturbations*, arXiv:2302.00344.
Their Eq. (4) is

    T_β^SM = [ (125/108) α_Y² − (95/72) α_2² − (49/6) α_3² ] T⁴ ≡ c_β^SM T⁴

which is exactly this repository's `c_beta`. TB state the group data they use explicitly —
`U(1)_Y`: `d_A = 1, C_A = 0, S_F = Σ Y_i² = 5`; `SU(2)_L`: `d_A = 3, C_A = 2, S_F = 3`;
`SU(3)`: `d_A = 8, C_A = 3, S_F = 3` — and these reproduce every `b_a` used here. They quote
`α_Y = 0.0181, α_2 = 0.0203, α_3 = 0.0189` at the Planck scale and obtain `c_β = −0.0031`, and they
write "The SU(3) contribution comprises 95% of the total." Their Eq. (16) is
`n_s ≈ 1 − 7α_3(M_P)/π = 0.958`.

**Epistemic status of [TB23], in their own words.** The tilt analysis is introduced as follows:
"We shall now give a heuristic analysis which, as it turns out, gives a remarkably accurate match
to the observations. **However, we caution the reader that our result rests on some key theoretical
assumptions which we have yet to verify.**" The abstract qualifies the results as holding "subject
to two simple theoretical assumptions". The paper is a February 2023 arXiv preprint; no journal
version was located, and it has five citations.

**[AZ95]** Arnold & Zhai, *Three-loop free energy for high-temperature QED and QCD with fermions*,
Phys. Rev. D **51**, 1906. **This is the true primary source for the coefficient**; TB quote its
Eq. (5.1). Two consequences worth stating:

* the expression is derived for QED and QCD with fermions, and TB obtain the `SU(2)_L` row by
  applying the same general group formula. The full Standard Model high-temperature pressure was
  computed separately by **Gynther & Vepsäläinen (2006)**;
* **no fundamental scalar contributes**, which is why `b_Y = −20/3` and `b_2 = 10/3` rather than the
  textbook SM `−41/6` and `19/6`. The difference is exactly `1/6` in each case — the Higgs-doublet
  term. This is consistent with TB's premise that the Higgs doublet is *emergent*, not fundamental.

**[Bu13]** Buttazzo et al., *Investigating the near-criticality of the Higgs boson*,
JHEP **12** (2013) 089 — the source of the three Planck-scale couplings, and therefore of every
number this repository prints.

**Observational comparison.** `Planck2018X` (*Planck 2018 results X: constraints on inflation*)
gives `n_s = 0.9587 ± 0.0056`, the value TB compare against. In this repository's terms that is an
**OBSERVATION**; TB's `0.958` is a **MODEL OUTPUT** of a heuristic mapping; the couplings are
**MODEL INPUT**. The numerical agreement of two numbers is a **HEURISTIC MATCH** and establishes
nothing about the mechanism.

**Contested status.** `ClineHell2026` (*Pathologies of dimension-zero scalar fields*,
Phys. Rev. D **114**, 045022) is a refereed paper examining precisely the claim that fourth-order
`(□φ)²` scalars cancel Standard Model loop contributions and that their fluctuations source the
primordial perturbations, and it identifies pathologies. `MillerVolovikZubkov2022` develops the
zero-dimension-scalar line. This repository takes **no position** on the mechanism — but the
proposal is contested in the refereed literature, not merely unverified by its authors, and a
reader should be told so.

## 2. The trace anomaly and beta functions — convention background

For the trace anomaly of a gauge theory in terms of the beta function, the standard references are
**Collins, Duncan & Joglekar (1977)** and, for the Weyl-anomaly side that TB's local cancellation
addresses, **Duff (1994)**.

For the one-loop coefficient and its sign structure, **Gross & Wilczek (1973)** and
**Caswell (1974)** (two loop). At one loop, `b_a = (11/3)C_A − (4/3)S_F` separates cleanly into a
gauge-self-interaction (antiscreening) term and a matter (screening) term, which is what makes the
repository's level-2 refinement well defined *at that order*. The `U(1)_Y` channel is positive
because `C_A = 0` leaves only the screening term — this is standard and is exactly TB's own table.

**Beyond one loop the separation is not clean**, and this is the literature that supports the
repository's own order-dependence warning: **Machacek & Vaughn (1983)** give the two-loop RGEs of a
general quantum field theory, in which the gauge beta functions contain terms mixing different gauge
couplings as well as Yukawa and scalar contributions; **Mihaila, Salomon & Steinhauser (2012)** give
the SM gauge beta functions to three loops. So a per-gauge-factor channel list is **not closed**
beyond leading order, and assigning mixed terms to channels requires an explicit convention. This
*complicates* the level-1/level-2 decomposition; it does not invalidate it at the order where it is
defined.

## 3. The mathematics — what the descriptors already are

**Signed measures.** Read the signed vector `c` as a discrete finite signed measure `μ`. Jordan
decomposition (`Bogachev2007`) gives `μ = μ⁺ − μ⁻` and `|μ| = μ⁺ + μ⁻`, so

    net   = μ(X)   = P − N      (total signed mass)
    gross = |μ|(X) = P + N      (total variation mass)
    kappa = 1 − |μ(X)|/|μ|(X) = 2 min(P, N) / (P + N)

Every result in the invariance audit follows from two textbook facts: **finite additivity** (net is
refinement-invariant) and **the triangle inequality with its equality case** (gross is
non-decreasing under refinement, with equality exactly when the split is sign-homogeneous). The
monotonicity of `kappa` is then immediate. These are elementary, and the repository's README already
describes its blindness result as "near-trivial as mathematics" — the same is true here.

*A caution the audit brief rightly flags:* the **total variation norm of a signed measure** is what
appears here. It is **not** the total variation *distance* between probability measures, and the two
must not be conflated. Only the former is used.

**The cancellation index already has a name.** In numerical analysis, the error bound for the
floating-point sum `Σx_i` carries the factor `Σ|x_i| / |Σx_i|`, which is the **condition number of
the sum** (`Higham1993`, `Higham2002`). That is exactly `gross/|net|`, so

    cond  = gross/|net| = 1/(1 − kappa)        kappa = 1 − 1/cond

Both directions are exact, so `kappa` is a **bounded reparameterization of a textbook quantity**,
not a new index. Its only advantage over `cond` is that it lives in `[0,1]` instead of `[1,∞]`.
This is the closest prior art found, and the repository should introduce `kappa` by way of it.

**The `2min/(sum)` form.** `2 min(P,N)/(P+N)` coincides formally with the Sørensen–Dice
coefficient `2|A∩B|/(|A|+|B|)` (`Dice1945`). This is a formal resemblance in a different
application, recorded for completeness and tagged as uncertain, not offered as prior art for the
physics.

**Blindness is non-identifiability.** "An observable that depends only on the sum cannot resolve
the terms inside it" is the statement that a many-to-one observation map loses what it collapses —
standard non-identifiability (`Rothenberg1971`). That an *even* function additionally loses the
sign is the same observation applied twice.

**Signed compositions.** The README correctly refuses to treat a mixed-sign vector as a probability
simplex or to apply Fisher information geometry to it. The audit confirms the framework that *does*
apply is signed-measure total variation, as above — no signed-simplex geometry is needed, and none
closer than the elementary `L¹` treatment was found.

## 4. What is left

With the physics imported and the mathematics classical, what remains is the **combination**: a
systematic decomposition-level reading of one specific coefficient, asking what the two observables
can and cannot see. No prior analysis of the Turok–Boyle coefficient along these lines was
identified — its citation network is five papers and none of them does this. That makes the
application apparently distinct while the ingredients are not, and the wording used throughout is
*"no equivalent analysis was identified in the literature reviewed"*, never a claim of priority.

## References

* **[AZ95]** P. B. Arnold and C. X. Zhai, "The three-loop free energy for high-temperature QED and QCD with fermions", *Phys. Rev. D* **51** (1995), 1906–1918. DOI: [10.1103/PhysRevD.51.1906](https://doi.org/10.1103/PhysRevD.51.1906).
* **[Ba23]** A. O. Barvinsky and W. Wachowski, "Notes on conformal anomaly, nonlocal effective action, and the metamorphosis of the running scale", *Phys. Rev. D* **108** (2023), 045014. DOI: [10.1103/PhysRevD.108.045014](https://doi.org/10.1103/PhysRevD.108.045014).
* **[Bo07]** V. I. Bogachev, *Measure Theory*, Springer, 2007. DOI: [10.1007/978-3-540-34514-5](https://doi.org/10.1007/978-3-540-34514-5). (Jordan/Hahn decomposition, total variation.)
* **[BT21]** L. Boyle and N. Turok, "Cancelling the vacuum energy and Weyl anomaly in the standard model with dimension-zero scalar fields", arXiv:2110.06258. DOI: [10.48550/arXiv.2110.06258](https://doi.org/10.48550/arXiv.2110.06258).
* **[Bu13]** D. Buttazzo, G. Degrassi, P. P. Giardino, G. F. Giudice, F. Sala, A. Salvio and A. Strumia, "Investigating the near-criticality of the Higgs boson", *JHEP* **12** (2013), 089. DOI: [10.1007/JHEP12(2013)089](https://doi.org/10.1007/JHEP12%282013%29089).
* **[Ca74]** W. E. Caswell, "Asymptotic behavior of non-abelian gauge theories to two-loop order", *Phys. Rev. Lett.* **33** (1974), 244–246. DOI: [10.1103/PhysRevLett.33.244](https://doi.org/10.1103/PhysRevLett.33.244).
* **[CDJ77]** J. C. Collins, A. Duncan and S. D. Joglekar, "Trace and dilatation anomalies in gauge theories", *Phys. Rev. D* **16** (1977), 438–449. DOI: [10.1103/PhysRevD.16.438](https://doi.org/10.1103/PhysRevD.16.438).
* **[CH26]** J. M. Cline and A. Hell, "Pathologies of dimension-zero scalar fields", *Phys. Rev. D* **114** (2026), 045022. DOI: [10.1103/63ck-c9rh](https://doi.org/10.1103/63ck-c9rh).
* **[Di45]** L. R. Dice, "Measures of the amount of ecologic association between species", *Ecology* **26** (1945), 297–302. DOI: [10.2307/1932409](https://doi.org/10.2307/1932409).
* **[Du94]** M. J. Duff, "Twenty years of the Weyl anomaly", *Class. Quantum Grav.* **11** (1994), 1387–1403. DOI: [10.1088/0264-9381/11/6/004](https://doi.org/10.1088/0264-9381/11/6/004).
* **[GV06]** A. Gynther and M. Vepsäläinen, "Pressure of the standard model at high temperatures", *JHEP* **01** (2006), 060. DOI: [10.1088/1126-6708/2006/01/060](https://doi.org/10.1088/1126-6708/2006/01/060).
* **[GW73]** D. J. Gross and F. Wilczek, "Ultraviolet behavior of non-abelian gauge theories", *Phys. Rev. Lett.* **30** (1973), 1343–1346. DOI: [10.1103/PhysRevLett.30.1343](https://doi.org/10.1103/PhysRevLett.30.1343).
* **[Hi93]** N. J. Higham, "The accuracy of floating point summation", *SIAM J. Sci. Comput.* **14** (1993), 783–799. DOI: [10.1137/0914050](https://doi.org/10.1137/0914050).
* **[Hi02]** N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002. DOI: [10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).
* **[MV83]** M. E. Machacek and M. T. Vaughn, "Two-loop renormalization group equations in a general quantum field theory. I. Wave function renormalization", *Nucl. Phys. B* **222** (1983), 83–103. DOI: [10.1016/0550-3213(83)90610-7](https://doi.org/10.1016/0550-3213%2883%2990610-7).
* **[MSS12]** L. N. Mihaila, J. Salomon and M. Steinhauser, "Gauge coupling beta functions in the standard model to three loops", *Phys. Rev. Lett.* **108** (2012), 151602. DOI: [10.1103/PhysRevLett.108.151602](https://doi.org/10.1103/PhysRevLett.108.151602).
* **[MVZ22]** J. Miller, G. E. Volovik and M. A. Zubkov, "Fundamental scalar field with zero dimension from anomaly cancellations", *Phys. Rev. D* **106** (2022), 015021. DOI: [10.1103/PhysRevD.106.015021](https://doi.org/10.1103/PhysRevD.106.015021).
* **[Pl18X]** Y. Akrami et al. (Planck Collaboration), "Planck 2018 results. X. Constraints on inflation", *Astron. Astrophys.* **641** (2020), A10. DOI: [10.1051/0004-6361/201833887](https://doi.org/10.1051/0004-6361/201833887).
* **[Qu24]** J. Quintin, X. Chen and R. Ebadi, "Fingerprints of a non-inflationary universe from massive fields", *JCAP* **09** (2024), 026. DOI: [10.1088/1475-7516/2024/09/026](https://doi.org/10.1088/1475-7516/2024/09/026).
* **[Ro71]** T. J. Rothenberg, "Identification in parametric models", *Econometrica* **39** (1971), 577–591. DOI: [10.2307/1913267](https://doi.org/10.2307/1913267).
* **[TB23]** N. Turok and L. Boyle, "A Minimal Explanation of the Primordial Cosmological Perturbations", arXiv:2302.00344 [hep-ph] (2023). DOI: [10.48550/arXiv.2302.00344](https://doi.org/10.48550/arXiv.2302.00344).

Machine-readable records: [`../references.bib`](../references.bib).

# Claim 1 method

The verifier reconstructs the proof independently from two exact identities.

1. Normalize a scorer into
   `q_s = p_minus exp(s/tau)/Z_s`. Expanding conditional KL gives
   `L(s)-L*=tau E_x KL(p_plus||q_s)`.
2. Equality in KL forces
   `s=tau log(p_plus/p_minus)+g(x)`.
3. For two items with likelihood ratios `r_i>r_j`, swapping an inversion
   increases conditional AUC by
   `p_minus_i p_minus_j (r_i-r_j)>0`.

SymPy checks the algebraic substitutions and factorization. A separate exact
audit uses `fractions.Fraction` over all positive integer distributions with
support sizes 2–4 and weights 1–3, comparing every score permutation. This
finite audit is a stress test, not the basis of the universal verdict.

The negative control reverses the likelihood-ratio order. It must exit nonzero
and identify a concrete exact counterexample.


# Claim 1 source audit

Source: arXiv `2605.02116v3`, retrieved 2026-07-29 with the recorded explicit
User-Agent. Source archive SHA-256:
`2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`.

Anchors:

- `consistency.tex`, `\label{thm:CRL_consistency}`: “a minimizer of
  L(s) is a maximizer of E(s).”
- `consistency.tex`, `\label{lem:minimizer-L}`: the minimizers are exactly
  `s(x,y)=tau log(p_x+(y)/p_x-(y))+g(x)`.
- `consistency.tex`, `\label{lem:max_AUC}`: maximizers order items by the
  likelihood ratio.
- `appendix/proof_consistency.tex`, `\label{eq:L=KL}`: the excess contrastive
  risk is a conditional KL divergence.

The theorem itself states no explicit assumptions. Its formulas and proof
require `tau>0`, finite risks, and a positive finite density ratio on common
support. If these fail, a real-valued minimizer typically does not exist; that
makes the printed implication vacuous rather than a counterexample. The
certificate states these well-posedness conditions explicitly.


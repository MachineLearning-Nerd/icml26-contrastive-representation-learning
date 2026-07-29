# Source audit

- Source: arXiv 2605.02116v3 e-print.
- Retrieval date: 2026-07-29.
- Source SHA-256: `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`.
- Anchor: `consistency.tex`, Theorem 3.4, label `thm:compare_cl`; proof in `appendix/proof_consistency.tex`.
- Exact quantifier: every admissible score `s`, with `tau > 0`.
- Exact conclusion: `E* - E(s) <= sqrt((2/tau)(L(s)-L*))`.

The certificate retains the factor `2/tau`; it does not tune a tolerance from observed data.

# Source audit

- Source: arXiv 2605.02116v3, SHA-256 `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`, retrieved 2026-07-29.
- Anchors: Assumption 4.1 `ass:bounded_data`; Lemmas `lem:inner_crl`, `lem:outer_crl`; Theorem 4.5 `thm:CRL_gen`.
- Quantifier: probability at least `1-delta`, uniformly over every `w` in the bounded network class.
- Exact inner term: `2 exp(8B/tau) tau/m`.
- Exact outer term: `1/sqrt(n)` multiplied by displayed logarithmic and architecture factors.

The prose states `tilde-O(1/m+1/sqrt(n))`. Calling it strict log-free `O` would erase terms present in the theorem.

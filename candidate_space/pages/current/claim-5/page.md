# Claim 5 — inner/outer decomposition

**Current verdict: VERIFIED**, pending the formal cumulative run.

The two Section 4 decompositions are triangle **inequalities**, not additive
equalities. The checker verifies them, gives an exact counterexample to
equality, differentiates the paper's `m`-dependent upper-bound terms, and
recovers the leading balance points `m=sqrt(n)` for SCRL and `m=n` for SSCRL.

The result concerns decreasing upper bounds. It does not assert that the
unknown true generalization gap is monotone, and the comparison with prior
`m`-deteriorating bounds is made at fixed `n`.

- Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`
- Verifier: `.openresearch/artifacts/claim_5/verifier.py`
- Contract/certificate: `.openresearch/artifacts/claim_5/`
- Negative control: asserts decomposition equality; required exit is nonzero.

This exact audit rejects and supersedes the historical approximate-additivity
proxy.

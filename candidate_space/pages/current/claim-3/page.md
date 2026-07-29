# Claim 3 — SCRL generalization

**Current verdict: VERIFIED**, pending the formal cumulative run.

Under Assumption 4.1 and independent negatives per anchor, Theorem 4.5 holds
with probability at least `1-delta`, uniformly over all `w` in `W`. Its inner
term is exactly `2 exp(8B/tau) tau/m`; the outer term has a `1/sqrt(n)`
polynomial factor and explicit logarithmic and architecture multipliers.

The faithful summary is `tilde-O(1/m + 1/sqrt(n))`. This page does not erase
the logarithms or claim that the bound is tight.

- Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`
- Verifier: `.openresearch/artifacts/claim_3/verifier.py`
- Contract/certificate: `.openresearch/artifacts/claim_3/`
- Negative control: replaces triangle inequality by equality and deletes logs;
  required exit is nonzero.

This proof certificate supersedes the historical noisy K=6 slope fit.

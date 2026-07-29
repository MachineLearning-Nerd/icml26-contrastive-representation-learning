# Claim 4 — SSCRL generalization

**Current verdict: VERIFIED**, pending the formal cumulative run.

Under Assumption 4.1, one set of `m` negatives is shared by all `n` anchors and
is independent of the positive pairs. Theorem 4.6 holds with probability at
least `1-delta`, uniformly over `W`, with `1/sqrt(m)` and `1/sqrt(n)`
polynomial factors plus the theorem's logarithmic multipliers.

The faithful summary is `tilde-O(1/sqrt(m) + 1/sqrt(n))`, not strict log-free
big-O.

- Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`
- Verifier: `.openresearch/artifacts/claim_4/verifier.py`
- Contract/certificate: `.openresearch/artifacts/claim_4/`
- Negative control: substitutes independently resampled negatives; required
  exit is nonzero.

This proof certificate supersedes the historical K=6 fitted slope.

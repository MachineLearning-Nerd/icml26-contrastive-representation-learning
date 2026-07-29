# Claim 2 — calibration inequality

**Current verdict: VERIFIED**, pending the formal cumulative run.

The exact Theorem 3.4 contract is
`E* - E(s) <= sqrt((2/tau)(L(s)-L*))` for every admissible scorer with
`tau > 0` and finite risks. The checker reconstructs the KL/Pinsker/ranking/Jensen
proof chain and independently audits 4,672 finite distribution triples.

- Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`
- Source SHA-256: `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`
- Positive verifier: `.openresearch/artifacts/claim_2/verifier.py`
- Raw certificate: `.openresearch/artifacts/claim_2/proof_certificate.json`
- Negative control: coefficient 2 changed to 1; required exit is nonzero.

The finite audit is corroboration; the analytic certificate carries the universal
result. The historical K=6 interpolation check is not used.

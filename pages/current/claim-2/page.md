# Claim 2 — Theorem 3.4 calibration

**Current verdict: VERIFIED.** This supersedes the **Historical rejected baseline**
at judged revision `302f93efc3f480fc58029255717998691d765314`.

## Exact claim contract

For positive `τ`, downstream retrieval suboptimality is at most `sqrt((2/τ)(L(s)-L*))` for every admissible scorer under the theorem's population distributions.

## Source and assumptions

The source is arXiv v3, retrieved 2026-07-29, SHA-256 `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`. The
certificate preserves the theorem's assumptions and quantifiers; finite checks
are stress tests, not the universal proof.

## Evidence

The certificate reconstructs the KL excess-risk identity, applies Pinsker with the exact coefficient 2, then the ranking and Jensen steps. An independent exact audit checks **4,672 distribution triples** with zero violations. Replacing coefficient 2 by 1 is rejected and exits 1.

| Required item | Evaluator-visible location |
| --- | --- |
| Contract and source audit | [claim contract](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/claim_contract.json), [source audit](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/source_audit.md) |
| Executable verifier | [verifier source](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/verifier.py) |
| Certificate/raw JSON | [positive certificate](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/proof_certificate.json) |
| Negative control | [mutated certificate](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/negative_control.json) |
| Exact output | [formal summary](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/formal_run_summary.json), [full raw log](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/formal_run.log) |
| Method and limitations | [method](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/method.md), [limitations](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_2/limitations.md) |

Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`  
Winning Git SHA: `aa5a6f11c751cb2c2428f0f2c85495565b06678e`  
Formal run: `b87faa51-053f-47e2-b886-ff2e5f1bef56` on Hugging Face `cpu-upgrade`; estimated 1 core, actual
allocation 64 logical/available CPUs, verifier runtime 24.729709 s. Deterministic
exact arithmetic; no stochastic seeds are needed.

## Limitation

The finite audit is deliberately secondary; it cannot alone prove a universal inequality.

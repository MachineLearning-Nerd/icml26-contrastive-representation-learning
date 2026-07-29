# Claim 5 — Section 4 inner/outer decomposition

**Current verdict: VERIFIED.** This supersedes the **Historical rejected baseline**
at judged revision `302f93efc3f480fc58029255717998691d765314`.

## Exact claim contract

The generalization bound is a triangle-inequality decomposition into inner negative-sampling error and outer anchor-sampling error; the derived bounds decrease with `m`, unlike the prior comparison bound proportional to `log(m)/sqrt(n)`.

## Source and assumptions

The source is arXiv v3, retrieved 2026-07-29, SHA-256 `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`. The
certificate preserves the theorem's assumptions and quantifiers; finite checks
are stress tests, not the universal proof.

## Evidence

The symbolic audit checks the two triangle inequalities, derivative signs, balance points, and the scope of the prior bound. It explicitly rejects the historical toy page's approximate additive equality. The equality mutation exits 1.

| Required item | Evaluator-visible location |
| --- | --- |
| Contract and source audit | [claim contract](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/claim_contract.json), [source audit](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/source_audit.md) |
| Executable verifier | [verifier source](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/verifier.py) |
| Certificate/raw JSON | [positive certificate](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/proof_certificate.json) |
| Negative control | [mutated certificate](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/negative_control.json) |
| Exact output | [formal summary](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/formal_run_summary.json), [full raw log](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/formal_run.log) |
| Method and limitations | [method](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/method.md), [limitations](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_5/limitations.md) |

Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`  
Winning Git SHA: `aa5a6f11c751cb2c2428f0f2c85495565b06678e`  
Formal run: `b87faa51-053f-47e2-b886-ff2e5f1bef56` on Hugging Face `cpu-upgrade`; estimated 1 core, actual
allocation 64 logical/available CPUs, verifier runtime 24.729709 s. Deterministic
exact arithmetic; no stochastic seeds are needed.

## Limitation

The result is a bound decomposition, not an empirical identity between measured gaps.

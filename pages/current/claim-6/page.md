# Claim 6 — Section 5 CLIP scaling

**Current verdict: BLOCKED.** This is not VERIFIED and not FALSIFIED.

## Exact claim contract and source

Section 5 reports FastCLIP training on DFN subsets with `n∈{6M,10M,14M}`,
five negative ratios `m/n∈{1%,10%,40%,70%,100%}`, shared negatives, and 320M
processed samples per model. It states that performance improves up to a
critical negative count and then saturates, with critical `m` scaling nearly
linearly in `n`. Source: arXiv v3, retrieved 2026-07-29, SHA-256
`2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`.

## Four completed routes

1. **Original vector extraction:** all 45 plotted values recovered. Every curve
   gains at least 7.59 points from 10% to 40%; the maximum 40–100% range is
   1.42. Critical points are exactly `m=0.4n`; a free-coefficient power fit is
   `m=0.4n` (exponent 1.0), while forcing unit coefficient yields 0.942872.
2. **Independent raster digitization:** all 45 points recovered independently,
   median absolute error 0.024478 and maximum 0.769378 points.
3. **Release audit:** exact execution needs at least 15 models and 4.8B processed
   samples without repeats. Paper-specific configuration, raw tables,
   checkpoints, seeds, uncertainty, DFN split IDs, and negative-subset IDs are
   unavailable.
4. **Dedicated falsification:** no assumption-satisfying contradiction was
   established. Small declines (`-0.25`, `-0.09`) lack uncertainty; positive/
   negative independence is not documented. An injected precritical reversal
   was detected and exited nonzero.

| Required item | Evaluator-visible location |
| --- | --- |
| Exact contract/source | [falsification contract](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_falsification/claim_contract.json), [source audit](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_falsification/source_audit.md) |
| Vector route code/data | [verifier](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_vector/verifier.py), [contract/raw values](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_vector/claim_contract.json) |
| Raster route | [verifier](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_raster/verifier.py), [contract](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_raster/claim_contract.json) |
| Release route | [audit](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_release/audit.py), [inventory](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_release/release_inventory.json) |
| Falsification/control | [verifier](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_falsification/verifier.py), [raw reported points](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_falsification/reported_points.json), [injected control](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/artifacts/claim_6_falsification/negative_control.json) |
| Exact output | [formal summary](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/formal_run_summary.json), [full raw log](https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/evidence/current/formal_run.log) |

Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`  
Winning Git SHA: `aa5a6f11c751cb2c2428f0f2c85495565b06678e`  
Formal run: `b87faa51-053f-47e2-b886-ff2e5f1bef56` on Hugging Face `cpu-upgrade`; estimated 1 core, actual
allocation 64 logical/available CPUs, verifier runtime 24.729709 s.

## Why BLOCKED

The figures strongly corroborate the paper's own displayed results, but they
are not an independent training reproduction. The absent configuration/data
identities/raw runs/uncertainty prevent faithful CPU-only execution and valid
falsification. Missing evidence is not converted into a pass.

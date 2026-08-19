# Claim-to-evidence ledger

This repository audits six source-anchored claims from *Statistical
Consistency and Generalization of Contrastive Representation Learning*. Each
row records the paper anchor, the production path, the control, and the exact
boundary of the verdict.

| Claim | Paper anchor | How the result is produced | Evidence and control | Scope and status |
| --- | --- | --- | --- | --- |
| C1 — likelihood-ratio ranking | Theorem 3.1 | Reconstruct the KL equality condition, pairwise exchange identity, and positive-temperature order preservation; then exhaustively audit 7,371 exact distributions and 162,000 rankings. | `.openresearch/artifacts/claim_1/proof_certificate.json` and `checker.py`; `negative_control.json` reverses the ranking and fails. | The symbolic certificate carries the theorem; finite exact audits stress the stated contract. **VERIFIED_SCOPED** |
| C2 — calibration inequality | Theorem 3.4 | Chain the KL excess-risk identity through Pinsker, ranking, and Jensen with coefficient 2; audit 4,672 exact distribution triples. | `.openresearch/artifacts/claim_2/proof_certificate.json` and `verifier.py`; coefficient-1 mutation is rejected. | The source assumptions and exact coefficient are retained. **VERIFIED_SCOPED** |
| C3 — SCRL generalization | Theorem 4.5 | Check bounded-class assumptions, probability and uniform quantifiers, the exact inner `1/m` term, outer tilde rate, and triangle combination. | `.openresearch/artifacts/claim_3/proof_certificate.json` and `verifier.py`; erasing logarithms and replacing the triangle inequality with equality fails. | The displayed logarithmic factors and quantifiers are preserved; finite checks do not replace the proof. **VERIFIED_SCOPED** |
| C4 — SSCRL generalization | Theorem 4.6 | Verify one shared negative set, independence assumptions, the `~1/sqrt(m)` and `~1/sqrt(n)` terms, and their logarithmic multipliers. | `.openresearch/artifacts/claim_4/proof_certificate.json` and `verifier.py`; independent negatives and a changed rate fail the control. | Verified only for the paper’s shared-negative contract. **VERIFIED_SCOPED** |
| C5 — inner/outer decomposition | Section 4 | Reconstruct both triangle inequalities, derivative signs, balance points, the decreasing SCRL term, the SSCRL terms, and the prior-bound scope. | `.openresearch/artifacts/claim_5/proof_certificate.json` and `verifier.py`; the historical additive-equality proxy is rejected. | This is an inequality/decomposition audit, not a claim that the terms are empirically equal. **VERIFIED_SCOPED** |
| C6 — FastCLIP scaling | Section 5 | Recover 45 vector-figure values, independently digitize the raster figures, fit the critical points, audit the minimum workload, and run a dedicated falsification route. | `.openresearch/artifacts/claim_6_vector`, `claim_6_raster`, `claim_6_release`, and `claim_6_falsification`; injected reversal is detected, but no valid contradiction is established. | Figures corroborate `m=0.4n`; missing configs, data IDs, raw runs, checkpoints, seeds, and uncertainty block training reproduction. **BLOCKED_RELEASE** |

## Evidence ladder

1. The paper source is pinned by SHA-256
   `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`.
2. Each positive route has a source audit, claim contract, executable checker,
   raw result or certificate, and a deliberately invalid control.
3. Exact finite counts are stress evidence. Universal statements remain tied to
   the reconstructed symbolic theorem contract and the paper’s assumptions.
4. Figure recovery is evidence preservation. It is not an independent
   reproduction of the authors’ large-scale CLIP training.

The complete path inventory is in [`EVIDENCE_MANIFEST.json`](EVIDENCE_MANIFEST.json).

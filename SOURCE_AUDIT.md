# Source audit entry point

## Primary source

- Paper: *Statistical Consistency and Generalization of Contrastive Representation Learning*
- Authors: Yuanfan Li, Xiyuan Wei, Tianbao Yang, and Yiming Ying
- arXiv: [2605.02116](https://arxiv.org/abs/2605.02116)
- Source used for the Section 5 audit: arXiv v3 e-print, retrieved 2026-07-29
- Source URL: <https://export.arxiv.org/e-print/2605.02116v3>
- Source SHA-256: `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`
- ICML submission identifier: `xixoixLXCr`

## Version and claim mapping

The current claim pages follow the paper’s displayed numbering: Theorem 3.1
for likelihood-ratio ranking, Theorem 3.4 for calibration, Theorem 4.5 for
SCRL, Theorem 4.6 for SSCRL, Section 4 for the decomposition, and Section 5
for the FastCLIP experiment. The inherited judged Space revision and its
historical evidence are retained under the paths recorded in
[`evidence/current/historical_subset_audit.json`](evidence/current/historical_subset_audit.json).

The generic FastCLIP implementation at
<https://github.com/Optimization-AI/FastCLIP> is recorded as infrastructure
only. The release audit found no paper-specific code/configuration URL, raw
Section 5 table, checkpoint, seed record, uncertainty record, DFN split ID, or
negative-subset ID.

## Fidelity boundary

Claims 1–5 preserve the cited assumptions, quantifiers, inequalities, rates,
and controls in machine-readable certificates. The exact finite audits support
those reconstructed contracts but do not replace the paper’s universal proofs.
Claim 6 preserves and cross-checks the displayed figures, but missing training
inputs prevent an independent rerun or a valid falsification.

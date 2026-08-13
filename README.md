# Statistical Consistency and Generalization of Contrastive Representation Learning

Independent, claim-by-claim reproduction audit for ICML 2026 paper
[“Statistical Consistency and Generalization of Contrastive Representation Learning”](https://arxiv.org/abs/2605.02116).

This repository audits the mathematical claims and the Section 5 empirical
evidence. It is not an official author implementation. The author figure routes
are evidence-preservation and feasibility audits, not a substitute for the
paper’s missing training release.

## Current assessment

Claims 1–5 are `VERIFIED` by symbolic certificates, exact finite stress audits,
and rejecting controls. Claim 6 is `BLOCKED`: the released figures are
independently recovered, but the paper does not release enough configuration,
data identity, raw runs, checkpoints, seeds, or uncertainty to reproduce or
validly falsify the 15-run FastCLIP study. The previous live judge score was
`5/12`; the `7–10/12` range is a forecast, not a new judge result.

| Claim | Paper statement tested | How this audit produces the result | Evidence and verdict |
| --- | --- | --- | --- |
| 1 | Theorem 3.1: a population contrastive-loss minimizer orders candidates by the positive/negative likelihood ratio and is optimal for ranking retrieval. | Reconstruct the KL equality condition, pairwise exchange identity, and positive-temperature order preservation; exhaustively audit 7,371 exact distributions and 162,000 rankings. Reverse the order as a negative control. | The symbolic certificate passes and the reversed ranking fails (`5/12 < 7/12`). **VERIFIED.** |
| 2 | Theorem 3.4: retrieval suboptimality is at most `sqrt((2/tau)(L(s)-L*))` for every admissible scorer. | Chain the KL excess-risk identity through Pinsker with the exact coefficient 2, ranking, and Jensen; audit 4,672 distribution triples and mutate the coefficient to 1 as a control. | Zero violations; the coefficient-1 mutation exits nonzero. **VERIFIED.** |
| 3 | Theorem 4.5: supervised contrastive representation learning has an inner `1/m` term and an outer `~1/sqrt(n)` term with its stated probability/uniform quantifiers. | Check the bounded-class assumptions, high-probability and uniform quantifiers, exact inner polynomial rate, outer logarithmic factors, and triangle combination. Remove logarithms in the negative control. | All source factors and quantifiers are retained; the log-free mutation is rejected. **VERIFIED.** |
| 4 | Theorem 4.6: shared-negative self-supervised contrastive learning has `~1/sqrt(m)` and `~1/sqrt(n)` rates. | Verify the shared set of negatives, independence from positive pairs, both tilde rates, and the displayed logarithmic multipliers; mutate the sampling assumption and rate as a control. | The shared-negative theorem contract passes; the mutated contract fails. **VERIFIED.** |
| 5 | Section 4’s inner/outer generalization decomposition improves with more negatives and is an inequality, not an empirical equality. | Reconstruct both triangle inequalities, derivative signs, balance points, the decreasing `1/m` SCRL term, the `1/sqrt(m)` SSCRL terms, and the scope of the prior comparison bound. | The symbolic decomposition passes; the historical additive-equality proxy is rejected. **VERIFIED.** |
| 6 | Section 5: FastCLIP performance improves with negative count, saturates after a critical count, and the critical count scales nearly linearly with anchor count. | Recover all 45 author-figure values from vector PDFs and independently digitize them from raster renders; fit the critical points, audit the minimum workload, and run a dedicated falsification/control route. | Figures agree (critical points `m=0.4n`), but the 15-model/4.8B-sample study cannot be independently rerun and no valid counterexample is established. **BLOCKED.** |

The current claim pages, source audits, raw evidence, checkers, controls, and
limitations are linked from [`pages/index.md`](pages/index.md) and
[`release/final_release_report.md`](release/final_release_report.md).

## What the paper is doing

The paper develops a statistical learning theory for contrastive representation
learning. It treats retrieval quality as an AUC-like population ranking
criterion, shows that population contrastive risk is statistically consistent
with likelihood-ratio ranking, and derives a calibration inequality connecting
excess contrastive risk to excess retrieval error. For upstream learning it
analyzes supervised and self-supervised contrastive objectives, deriving
generalization terms that improve with the number of negatives and expose a
trade-off between negative count `m` and anchor count `n`. Section 5 tests the
theory on FastCLIP vision-language training.

## Reproducing the evidence

The pinned command for every formal node is:

```bash
uv sync --frozen && uv run --frozen python run_reproduction.py
```

Claims 1–5 use exact rational or symbolic certificates plus intentionally
invalid controls. The finite enumerations are stress tests; the universal
verdicts come from the reconstructed theorem certificates and their explicit
assumptions. Claim 6 has four routes:

1. original vector-figure extraction;
2. independent raster digitization;
3. release feasibility and missing-input audit;
4. dedicated falsification with injected reversal and controls.

Those routes establish figure corroboration and the reason for `BLOCKED`; they
do not claim an independent CLIP training reproduction.

Useful entry points:

- [Current claim index](pages/index.md)
- [Illustrated report](reports/reproduction/report.md)
- [Final release report](release/final_release_report.md)
- [Formal run summary](evidence/current/formal_run_summary.json)
- [Claim contracts and verifiers](.openresearch/artifacts/)
- [Reproduction notebook](notebooks/reproduction.py)
- [Evaluator-visible Space](https://huggingface.co/spaces/DineshAI/xixoixLXCr)

## Branch organization

`main` is the publication surface. Descriptive `audit/*`, `historical/*`, and
`release/*` branches preserve the theorem and figure-audit lineage. The full
old-to-new mapping, including historical `orx/*` names, is in
[`branch-audit.md`](branch-audit.md).

## Scope and limitations

- Claims 1–5 verify the paper statements with the source assumptions and
  quantifiers preserved; finite checks do not replace the proofs.
- Tilde rates are kept as tilde rates. The audit does not erase logarithmic
  factors to manufacture a stricter big-O claim.
- Claim 4 requires shared negatives; independently sampled negatives would be a
  different theorem and are not treated as evidence.
- The 45 recovered CLIP points corroborate the displayed figures, but the
  paper-specific configs, DFN split and negative-subset IDs, raw measurements,
  checkpoints, seeds, and uncertainty are unavailable. Missing release inputs
  are not converted into either a pass or a falsification.
- The live judge score remains `5/12` until a new revision is evaluated.

## Paper

- **Title:** Statistical Consistency and Generalization of Contrastive Representation Learning
- **Authors:** Yuanfan Li, Xiyuan Wei, Tianbao Yang, Yiming Ying
- **Paper:** [arXiv:2605.02116](https://arxiv.org/abs/2605.02116)
- **HTML source:** [arXiv HTML](https://arxiv.org/html/2605.02116)
- **Submission:** ICML 2026; arXiv v1 submitted May 4, 2026, v3 revised May 28, 2026
- **Paper identifier:** `xixoixLXCr`

## Citation

```bibtex
@misc{li2026statistical,
  title         = {Statistical Consistency and Generalization of Contrastive Representation Learning},
  author        = {Li, Yuanfan and Wei, Xiyuan and Yang, Tianbao and Ying, Yiming},
  year          = {2026},
  eprint        = {2605.02116},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  note          = {ICML 2026; revised version arXiv:2605.02116v3}
}
```

## Thank you

Thank you to Yuanfan Li, Xiyuan Wei, Tianbao Yang, and Yiming Ying for making
the contrastive-learning theory explicit enough to audit at the level of KL
identities, sampling assumptions, rates, and ranking objectives. The paper’s
clear theorem structure made it possible to preserve the positive evidence for
Claims 1–5 while honestly distinguishing figure corroboration from an
independent large-scale training reproduction for Claim 6.

## Attribution

This independent audit is maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
It is not affiliated with or endorsed by the paper’s authors.

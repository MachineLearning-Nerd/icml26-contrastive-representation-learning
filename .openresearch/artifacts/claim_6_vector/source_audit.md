# Section 5 source audit

- Source: arXiv 2605.02116v3 e-print.
- Retrieved: 2026-07-29 with explicit `OpenResearch-Reproduction/1.0` user-agent.
- SHA-256: `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`.
- Anchor: `experiment_conclusion.tex`, Section 5.
- Domain: FastCLIP training on DFN subsets described as 6M, 10M, and 14M anchors.
- Negative ratios: `m/n` in `{0.01, 0.1, 0.4, 0.7, 1.0}`.
- Budget: 320M processed samples for every `(n,m)` pair.
- Metrics: ImageNet zero-shot top-1; mean image/text recall@1 on MSCOCO and Flickr.

No code URL, raw table, checkpoints, random seeds, repeated-run uncertainty, or
error bars are supplied in the paper source.

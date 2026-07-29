# Claim 6 — Section 5 CLIP evidence

**Current verdict: BLOCKED.**

The paper reports 15 FastCLIP runs on DFN subsets of 6M, 10M, and 14M anchors,
five `m/n` ratios, and 320M processed samples per run. No code URL, checkpoints,
raw table, seeds, repeated-run uncertainty, or error bars are released.

Route 1 independently parses the original vector PDFs from the exact hashed
arXiv source. It recovers all 45 reported performance values. Every curve gains
at least five points from 10% to 40% negatives, then varies by at most 1.5
points through 100%. The critical points are exactly `m=0.4n`: a free-coefficient
power fit has exponent 1.0, while forcing coefficient 1 produces about 0.943.

This corroborates what the author figures encode; it does not independently
reproduce CLIP training.

Three verification routes and the mandatory fourth falsification route were
completed:

1. Vector extraction: all 45 values recovered.
2. Independent raster digitization: median error 0.024 points, maximum 0.77.
3. Release audit: exact training requires at least 15 models and 4.8B processed
   samples, but paper-specific code/configuration, subsets, checkpoints, raw
   runs, seeds, and uncertainty are unavailable.
4. Dedicated falsification: no assumption-satisfying contradiction was found.
   An injected precritical reversal was correctly detected. Missing independence
   evidence and uncertainty were not misreported as falsification.

The final Claim 6 result is therefore **BLOCKED**, not FALSIFIED.

- Fixed command: `uv sync --frozen && uv run --frozen python run_reproduction.py`
- Verifier: `.openresearch/artifacts/claim_6_vector/verifier.py`
- Source SHA-256: `2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764`
- Negative control: expects four curves per task instead of three; required
  exit is nonzero.

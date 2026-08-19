# Audit report

## Executive result

Claims 1–5 pass their scoped symbolic and exact-audit contracts. Claim 6 is
blocked: the paper figures can be recovered and cross-checked, but the
paper-specific FastCLIP training release is incomplete. The only score claimed
is the historical external result `5/12`.

Overall status:

`PARTIAL_C1_C2_C3_C4_C5_VERIFIED_C6_BLOCKED_HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE`

## Claim matrix

| Claim | Result | Primary route | Main boundary |
| --- | --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | KL equality, pairwise exchange, exact ranking audit | Source certificate supplies the universal theorem; finite cases are stress evidence. |
| C2 | `VERIFIED_SCOPED` | KL–Pinsker calibration chain and 4,672 exact triples | Coefficient 2 is retained; coefficient 1 is a rejecting control. |
| C3 | `VERIFIED_SCOPED` | SCRL inner/outer rate and quantifier certificate | Logs and triangle inequality are retained; no log-free claim is made. |
| C4 | `VERIFIED_SCOPED` | SSCRL shared-negative rate certificate | The verdict is conditional on the paper’s shared-negative sampling contract. |
| C5 | `VERIFIED_SCOPED` | Section 4 decomposition and balance-point audit | The decomposition is an inequality, not an equality. |
| C6 | `BLOCKED_RELEASE` | Vector/raster figure recovery, release audit, falsification controls | No independent full-scale training or valid assumption-satisfying counterexample. |

## Quantitative evidence

- C1: 7,371 exact distributions and 162,000 rankings; the reversed-order
  control fails with candidate AUC `5/12` versus maximum `7/12`.
- C2: 4,672 distribution triples; the coefficient-1 mutation fails.
- C6: 45 author-figure values recovered; raster digitization median absolute
  error `0.024478` and maximum `0.769378` percentage points.
- C6: critical points satisfy `m=0.4n`; the free-coefficient power exponent is
  `1.0`, while the unit-coefficient fit gives the paper’s `0.942872`.
- C6: minimum workload is 15 models × 320M processed samples = 4.8B sample
  presentations before uncertainty repeats.

## Score and publication boundary

- Historical live score: `5/12`
- Current score claim: `false`
- Publication allowed: `false`
- Official author endorsement: `false` / not claimed

Open [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md) for production paths and
controls, and [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) for source/version scope.

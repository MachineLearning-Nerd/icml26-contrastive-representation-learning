Previous live judged score: `5/12`

Conservative projected score range after the proposed change: **7–10/12**

Best-supported possible new score: **10/12 (forecast, not a judge result)**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Universal symbolic certificate plus 7,371 exact distributions and 162,000 rankings; judge acceptance of the reconstructed proof certificate remains the scoring risk. |
| 2 | 1 | 2 | HIGH | VERIFIED | Exact KL–Pinsker–ranking chain and 4,672 exact stress cases; finite cases are not treated as universal proof. |
| 3 | 1 | 2 | HIGH | VERIFIED | Exact Theorem 4.5 high-probability/uniform quantifiers and logarithmic factors retained. |
| 4 | 1 | 2 | HIGH | VERIFIED | Exact shared-negative assumption and tilde rates retained. |
| 5 | 1 | 2 | HIGH | VERIFIED | Triangle-inequality decomposition proved; historical additive-equality proxy explicitly rejected. |
| 6 | 0 | 2 | LOW | BLOCKED | Four materially different routes completed; released figures corroborate the trend but cannot substitute for independent CLIP training or an assumption-satisfying falsification. |

# Final release report

Current total score: **5/12**. Conservative projected total score range:
**7–10/12**. Best-supported possible total: **10/12**, pending the live judge.
Claims 1–5 changed from TOY evidence to VERIFIED certificates. Claim 6 remains
BLOCKED because exact data/config identities, raw measurements, checkpoints,
seeds, and uncertainty are unavailable.

Baseline HF Head and Judge Head:
`302f93efc3f480fc58029255717998691d765314`. Baseline Git SHA:
`ee3144275b29190240eb4816b190690182f335d9`. Winning branch:
`orx/c6-dedicated-falsification`; winning Git SHA:
`aa5a6f11c751cb2c2428f0f2c85495565b06678e`.

## Experiment tree and compute

| Experiment | Commit | Run | Managed wall time | Outcome |
| --- | --- | --- | ---: | --- |
| Historical judged baseline | `97dddb0` | `10fddab1-357a-4992-a3ac-60b350474df7` | 21s | VERIFIED historical regression |
| C1 constructive proof certificate | `fe4f79e` | `f9faa7d8-1bbb-42dd-b6ac-3dd04f2dd335` | 32s | Claim 1 VERIFIED |
| C1 adversarial assumption audit | `0d36cde` | `1559ba55-8633-439a-b6b1-b5ea85554e42` | 26s | No valid counterexample |
| C2-C5 analytic certificates | `ee6d007` | `7d8a8f4c-60b9-40ce-a0ca-695885174453` | 37s | Claims 2–5 VERIFIED |
| C2-C5 falsification stress | `b95dd0c` | `46013220-34f8-4e43-9422-e13d9afd4401` | 37s | Literal log-free rate rejected |
| C6 vector figure extraction | `e8599c6` | `e7b20b91-81d6-4e37-b048-7f44cbbf906b` | 44s | Figures corroborated; Claim 6 BLOCKED |
| C6 raster digitization | `ebdfcf1` | `c2079d15-e104-48ff-a531-b2662c89504c` | 42s | Independent raster corroboration |
| C6 release feasibility audit | `fa4abfe` | `64689682-c98d-4d89-85de-8f8c52446d55` | 43s | Claim 6 BLOCKED |
| C6 dedicated falsification | `aa5a6f1` | `b87faa51-053f-47e2-b886-ff2e5f1bef56` | 1m04s | Claims 1–5 VERIFIED; Claim 6 BLOCKED |

All successful runs used Hugging Face `cpu-upgrade`; the cumulative verifier
estimated one core, observed 64 logical/available CPUs, and took 24.729709
seconds inside the job. Successful managed wall time totals **5m26s**; including
the preserved failed setup attempt, **5m36s**. Local smoke tests were one-core,
under five minutes (the cumulative smoke test took 9.395146 s). Provider billing
cost is **not exposed by the local `orx runs`/log evidence**, so no monetary
amount is invented.

## Evidence paths

- Canonical matrix: `pages/index.md`
- Claim pages: `pages/current/claim-1/page.md` through
  `pages/current/claim-6/page.md`
- Raw formal log: `evidence/current/formal_run.log`
- Machine-readable output: `evidence/current/formal_run_summary.json`
- Contracts/checkers/controls: `evidence/current/artifacts/`
- Blind reviews: `evidence/current/red_team_round_1.md` and
  `evidence/current/red_team_round_2.md`
- Historical subset proof: `evidence/current/historical_subset_audit.json`
- Illustrated report: `reports/reproduction/report.md`
- Tutorial notebook: `notebooks/reproduction.py`

## Release gates

The fixed command regenerates the raw results. Claims 1–5 and the historical
regression pass; every negative control exits nonzero. Claim 6 is visibly
BLOCKED after exactly four routes. No toy result is described as full-scale.
The 13 judged Space paths are a subset of the candidate; the historical evidence
page is byte-identical. `logbook.json` and all evidence JSON parse. The second
evaluator-blind traversal opened 61 files and found no missing visibility cell.
All report SVGs rendered successfully and `marimo check --strict` passed with
Marimo 0.23.1. Secret scanning and the text-only extension gate pass.

The exact upload paths are in `release/upload_allowlist.txt`; SHA-256 values are
in `release/upload_manifest.sha256`. Historical binaries are not reuploaded.

## Publication action

Commit only the allowlisted text files to the existing
`DineshAI/xixoixLXCr` Space, download the exact resulting revision, verify every
uploaded hash, rerun canonical traversal, then mirror the identical text paths
to GitHub `main` and confirm the remote SHA. No second Space is created. The
paper is marked awaiting judge; no score increase is claimed before a live
verdict.

See `release/commands.md` for the command record.

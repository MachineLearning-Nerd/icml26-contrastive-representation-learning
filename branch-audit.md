# Branch audit

The old `orx/*` names are retained here only as historical provenance. Each
branch was renamed to describe the claim or release role.

| Historical branch | Clean branch | Purpose |
| --- | --- | --- |
| `orx/historical-judged-baseline` | `historical/judged-baseline` | Preserve the earlier judged Space and toy-scale evidence. |
| `orx/c1-constructive-proof-certificate` | `audit/c1-fisher-consistency` | Build the Theorem 3.1 likelihood-ratio/Fisher-consistency certificate. |
| `orx/c1-adversarial-assumption-audit` | `audit/c1-adversarial-assumption` | Stress the Claim 1 assumptions and negative control. |
| `orx/c2-c5-analytic-certificates` | `audit/c2-c5-analytic-certificates` | Verify calibration, SCRL, SSCRL, and decomposition certificates. |
| `orx/c2-c5-falsification-stress` | `audit/c2-c5-control-stress` | Stress log factors, shared negatives, and inequality-vs-equality controls. |
| `orx/c6-vector-figure-extraction` | `audit/c6-vector-figure-extraction` | Recover the original vector-figure values. |
| `orx/c6-raster-digitization` | `audit/c6-raster-digitization` | Independently digitize the figures from rendered pixels. |
| `orx/c6-release-feasibility-audit` | `audit/c6-release-feasibility` | Audit missing configs, data identities, and the minimum Section 5 workload. |
| `orx/c6-dedicated-falsification` | `audit/c6-dedicated-falsification` | Run the cumulative suite and dedicated Claim 6 falsification/control route. |

`main` is the publication surface. Every clean branch receives this README and
branch map so an experiment checkout remains self-describing. Superseded
`orx/*` refs are deleted from the live GitHub repository after the clean refs
are published.

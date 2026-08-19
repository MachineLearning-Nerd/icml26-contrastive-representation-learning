# Environment and reproduction boundary

## Locked command

Run the cumulative audit from `main` with:

```bash
uv sync --frozen && uv run --frozen python run_reproduction.py
```

The Python dependency graph is pinned by [`uv.lock`](uv.lock). The formal and
certificate routes are deterministic and CPU-suitable; no random seed is
needed for Claims 1–5. Claim 6’s full training workload is not executable from
the released paper materials.

## What the command checks

- the historical judged-revision manifest and preserved historical paths;
- a positive certificate and an intentionally invalid control for Claims 1–5;
- exact distribution/ranking stress counts for Claims 1–2;
- source assumptions, logarithmic factors, shared negatives, and quantifiers
  for Claims 3–5;
- vector extraction, raster digitization, release feasibility, and dedicated
  falsification controls for Claim 6.

## Runtime boundary

The Section 5 release audit identifies at least 15 models and 4.8 billion
processed sample presentations before repeats for uncertainty. It also records
that paper-specific configuration, data identities, raw measurements,
checkpoints, seeds, and uncertainty are unavailable. A guessed implementation
would not be a faithful reproduction and is therefore not treated as evidence.

# Command record

No token values, generated job wrappers, or credentials are included.

## Startup and source audit

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 0e6f165b-7b2a-4b28-ab5a-20496239aac3
git rev-parse HEAD
git status --short
git branch -a
git worktree list --porcelain
df -h .
curl -A "OpenResearch-Reproduction/1.0" https://export.arxiv.org/e-print/2605.02116v3
curl -A "OpenResearch-Reproduction/1.0" https://ar5iv.labs.arxiv.org/html/2605.02116
```

The verdict dataset was fetched and filtered strictly by
`space_id == "DineshAI/xixoixLXCr"`. The exact judged Space revision
`302f93efc3f480fc58029255717998691d765314` was downloaded and hashed.
Environment inspection printed names only, never values.

## Fixed reproduction command

Every experiment inherited this exact command:

```bash
uv sync --frozen && uv run --frozen python run_reproduction.py
```

## Managed runs

- `Historical judged baseline`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `10fddab1-357a-4992-a3ac-60b350474df7`, commit `97dddb0`.
- `C1 constructive proof certificate`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `f9faa7d8-1bbb-42dd-b6ac-3dd04f2dd335`, commit `fe4f79e`.
- `C1 adversarial assumption audit`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `1559ba55-8633-439a-b6b1-b5ea85554e42`, commit `0d36cde`.
- `C2-C5 analytic certificates`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `7d8a8f4c-60b9-40ce-a0ca-695885174453`, commit `ee6d007`.
- `C2-C5 falsification stress`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `46013220-34f8-4e43-9422-e13d9afd4401`, commit `b95dd0c`.
- `C6 vector figure extraction`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `e7b20b91-81d6-4e37-b048-7f44cbbf906b`, commit `e8599c6`.
- `C6 raster digitization`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `c2079d15-e104-48ff-a531-b2662c89504c`, commit `ebdfcf1`.
- `C6 release feasibility audit`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `64689682-c98d-4d89-85de-8f8c52446d55`, commit `fa4abfe`.
- `C6 dedicated falsification`: `orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; run `b87faa51-053f-47e2-b886-ff2e5f1bef56`, commit `aa5a6f1`.

Each launch was followed by `orx exp wait <experiment-id> --timeout 480` and
`orx logs <run-id>`. One initial baseline job using an unsuitable UV image
failed with exit 127; it is retained as run
`7d9e3a6f-d65c-4b28-a31b-35c10b47b568`.

## Publication validation

```text
python3 tools/build_publication.py --winning-tree <winning-worktree> --judged-space <judged-snapshot> --candidate <fresh-candidate> --files-dir <project-files-dir>
python3 tools/audit_candidate.py <fresh-candidate> --mirror evidence/current/red_team_round_2.md
uvx --from marimo==0.23.1 marimo check --strict notebooks/reproduction.py
rsvg-convert reports/reproduction/images/<figure>.svg -o <temporary-png>
python3 tools/release_gate.py <fresh-candidate> --judged-space <judged-snapshot>
```

Read-only diagnostics used throughout were `rg`, `sed`, `find`, `git status`,
`git diff --check`, `git log`, `orx exp status`, `orx exp desc`, and
`orx runs`. Git writes were scoped `git add`, `git commit`, and `git push` on
the owned experiment branch or publication `main`.

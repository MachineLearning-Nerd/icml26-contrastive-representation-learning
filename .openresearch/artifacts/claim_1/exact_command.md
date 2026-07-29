# Exact command and environment

Inherited command:

```bash
uv sync --frozen && uv run --frozen python run_reproduction.py
```

Python is pinned to 3.12 and all packages are locked by `uv.lock`. Formal runs
use Hugging Face `cpu-upgrade` and
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

Estimated requirement: one CPU core, under one minute after dependency sync.


# Exact command

```bash
uv sync --frozen && uv run --frozen python run_reproduction.py
```

Estimated requirement: one core and under one minute after dependency sync.
Formal execution uses HF `cpu-upgrade` and the pinned uv Python 3.12 image.


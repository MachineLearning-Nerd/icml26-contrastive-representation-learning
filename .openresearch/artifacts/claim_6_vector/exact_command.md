# Exact command

`uv sync --frozen && uv run --frozen python run_reproduction.py`

Formal run uses Hugging Face `cpu-upgrade`. Estimated scientific need: one CPU
core; network and parsing runtime is uncertain. Actual allocation and runtime
are printed in raw output.

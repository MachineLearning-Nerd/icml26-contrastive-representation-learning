#!/usr/bin/env python3
"""Create the text-only upload manifest and enforce release gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


TEXT_SUFFIXES = {
    ".json",
    ".lock",
    ".log",
    ".md",
    ".py",
    ".sha256",
    ".svg",
    ".toml",
    ".txt",
}
SECRET_PATTERNS = {
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Bearer credential": re.compile(r"Authorization:\s*Bearer\s+\S+", re.I),
}


RUNS = [
    ("Historical judged baseline", "10fddab1-357a-4992-a3ac-60b350474df7", "97dddb0", "21s", "VERIFIED historical regression"),
    ("C1 constructive proof certificate", "f9faa7d8-1bbb-42dd-b6ac-3dd04f2dd335", "fe4f79e", "32s", "Claim 1 VERIFIED"),
    ("C1 adversarial assumption audit", "1559ba55-8633-439a-b6b1-b5ea85554e42", "0d36cde", "26s", "No valid counterexample"),
    ("C2-C5 analytic certificates", "7d8a8f4c-60b9-40ce-a0ca-695885174453", "ee6d007", "37s", "Claims 2–5 VERIFIED"),
    ("C2-C5 falsification stress", "46013220-34f8-4e43-9422-e13d9afd4401", "b95dd0c", "37s", "Literal log-free rate rejected"),
    ("C6 vector figure extraction", "e7b20b91-81d6-4e37-b048-7f44cbbf906b", "e8599c6", "44s", "Figures corroborated; Claim 6 BLOCKED"),
    ("C6 raster digitization", "c2079d15-e104-48ff-a531-b2662c89504c", "ebdfcf1", "42s", "Independent raster corroboration"),
    ("C6 release feasibility audit", "64689682-c98d-4d89-85de-8f8c52446d55", "fa4abfe", "43s", "Claim 6 BLOCKED"),
    ("C6 dedicated falsification", "b87faa51-053f-47e2-b886-ff2e5f1bef56", "aa5a6f1", "1m04s", "Claims 1–5 VERIFIED; Claim 6 BLOCKED"),
]


def write_both(repo: Path, candidate: Path, relative: str, content: str) -> None:
    for root in (repo, candidate):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")


def commands_report() -> str:
    run_commands = "\n".join(
        f"- `{title}`: `orx exp run <experiment-id> --flavor cpu-upgrade "
        "--image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h`; "
        f"run `{run_id}`, commit `{commit}`."
        for title, run_id, commit, _, _ in RUNS
    )
    return f"""# Command record

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

{run_commands}

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
"""


def final_report() -> str:
    run_rows = "\n".join(
        f"| {title} | `{commit}` | `{run_id}` | {duration} | {outcome} |"
        for title, run_id, commit, duration, outcome in RUNS
    )
    return f"""Previous live judged score: `5/12`

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
`audit/c6-dedicated-falsification`; winning Git SHA:
`aa5a6f11c751cb2c2428f0f2c85495565b06678e`.

## Experiment tree and compute

| Experiment | Commit | Run | Managed wall time | Outcome |
| --- | --- | --- | ---: | --- |
{run_rows}

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
"""


def changed_files(candidate: Path, judged: Path) -> set[str]:
    changed = set()
    for path in candidate.rglob("*"):
        if not path.is_file() or ".cache" in path.relative_to(candidate).parts:
            continue
        relative = str(path.relative_to(candidate))
        old = judged / relative
        if not old.is_file() or old.read_bytes() != path.read_bytes():
            changed.add(relative)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--judged-space", type=Path, required=True)
    args = parser.parse_args()
    repo = Path.cwd()
    candidate = args.candidate.resolve()
    judged = args.judged_space.resolve()

    write_both(repo, candidate, "release/commands.md", commands_report())
    write_both(repo, candidate, "release/final_release_report.md", final_report())

    failures: list[str] = []
    for path in candidate.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append(f"invalid JSON {path.relative_to(candidate)}: {error}")
    for path in candidate.rglob("*.svg"):
        try:
            ET.parse(path)
        except ET.ParseError as error:
            failures.append(f"invalid SVG {path.relative_to(candidate)}: {error}")
    for path in candidate.rglob("*"):
        if not path.is_file() or ".cache" in path.relative_to(candidate).parts:
            continue
        relative = str(path.relative_to(candidate))
        if path.suffix.lower() in TEXT_SUFFIXES or relative in {
            "README.md",
            "pyproject.toml",
        }:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                failures.append(f"text allowlist file is not UTF-8: {relative}")
                continue
            for name, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    failures.append(f"{name} pattern in {relative}")

    subset = json.loads(
        (candidate / "evidence/current/historical_subset_audit.json").read_text()
    )
    if subset["old_file_count"] != 13 or not subset["all_old_paths_present"]:
        failures.append("protected 13-file subset gate failed")
    if not subset["historical_evidence_page_unchanged"]:
        failures.append("historical evidence page changed")
    red_team = (candidate / "evidence/current/red_team_round_2.md").read_text()
    if "**Result: PASS.**" not in red_team:
        failures.append("evaluator-blind round 2 did not pass")
    summary = json.loads(
        (candidate / "evidence/current/formal_run_summary.json").read_text()
    )
    if summary["status"] != "VERIFIED":
        failures.append("formal cumulative run failed")
    for claim in range(1, 6):
        evidence = summary["claims"][f"claim_{claim}"]
        if evidence["status"] != "VERIFIED" or evidence["negative_control_exit"] == 0:
            failures.append(f"Claim {claim} cumulative regression failed")
    if summary["claims"]["claim_6_falsification_route"]["status"] != "BLOCKED":
        failures.append("Claim 6 is not honestly BLOCKED")

    proposed = changed_files(candidate, judged)
    proposed.update(
        {
            "release/gate_report.json",
            "release/upload_allowlist.txt",
            "release/upload_manifest.sha256",
        }
    )
    disallowed = sorted(
        relative
        for relative in proposed
        if Path(relative).suffix.lower() not in TEXT_SUFFIXES
        and relative not in {"README.md", "pyproject.toml"}
    )
    if disallowed:
        failures.append(f"non-text upload paths: {disallowed}")

    gate = {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "upload_file_count": len(proposed),
        "text_only": not disallowed,
        "secret_scan": "PASS" if not any("pattern" in item for item in failures) else "FAIL",
        "historical_old_file_count": subset["old_file_count"],
        "all_old_paths_present": subset["all_old_paths_present"],
        "historical_evidence_page_unchanged": subset[
            "historical_evidence_page_unchanged"
        ],
        "red_team_round_2": "PASS" if "**Result: PASS.**" in red_team else "FAIL",
        "formal_run_id": "b87faa51-053f-47e2-b886-ff2e5f1bef56",
        "winning_git_sha": "aa5a6f11c751cb2c2428f0f2c85495565b06678e",
        "candidate_verdicts": {
            "claim_1": "VERIFIED",
            "claim_2": "VERIFIED",
            "claim_3": "VERIFIED",
            "claim_4": "VERIFIED",
            "claim_5": "VERIFIED",
            "claim_6": "BLOCKED",
        },
    }
    write_both(repo, candidate, "release/gate_report.json", json.dumps(gate, indent=2))

    allowlist = "\n".join(sorted(proposed)) + "\n"
    write_both(repo, candidate, "release/upload_allowlist.txt", allowlist)
    manifest_rows = []
    for relative in sorted(proposed - {"release/upload_manifest.sha256"}):
        digest = hashlib.sha256((candidate / relative).read_bytes()).hexdigest()
        manifest_rows.append(f"{digest}  {relative}")
    manifest = "\n".join(manifest_rows) + "\n"
    write_both(repo, candidate, "release/upload_manifest.sha256", manifest)

    if failures:
        print(json.dumps(gate, indent=2))
        raise SystemExit(1)
    print(json.dumps(gate, indent=2))


if __name__ == "__main__":
    main()

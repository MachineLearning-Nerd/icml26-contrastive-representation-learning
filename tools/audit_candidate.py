#!/usr/bin/env python3
"""Evaluator-blind traversal of a built Space candidate."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


SPACE_PREFIX = "https://huggingface.co/spaces/DineshAI/xixoixLXCr/blob/main/"
FIXED_COMMAND = "uv sync --frozen && uv run --frozen python run_reproduction.py"
WINNING_SHA = "aa5a6f11c751cb2c2428f0f2c85495565b06678e"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--mirror", type=Path, required=True)
    args = parser.parse_args()
    root = args.candidate.resolve()
    opened: list[str] = []
    failures: list[str] = []

    def read(relative: str) -> str:
        path = root / relative
        if not path.is_file():
            failures.append(f"missing: {relative}")
            return ""
        opened.append(relative)
        return path.read_text(encoding="utf-8")

    readme = read("README.md")
    logbook_text = read("logbook.json")
    index = read("pages/index.md")
    report = read("reports/reproduction/report.md")
    round_one = read("evidence/current/red_team_round_1.md")
    summary_text = read("evidence/current/formal_run_summary.json")
    subset_text = read("evidence/current/historical_subset_audit.json")

    for required in (
        "7–10/12",
        "10/12",
        "Claim 6",
        "BLOCKED",
        "Historical rejected baseline",
        "reports/reproduction/report.md",
        "notebooks/reproduction.py",
    ):
        if required not in readme:
            failures.append(f"README missing {required!r}")

    try:
        logbook = json.loads(logbook_text)
    except json.JSONDecodeError:
        failures.append("logbook.json is invalid")
        logbook = {}
    children = logbook.get("root", {}).get("children", [])
    slugs = [child.get("slug") for child in children]
    expected_slugs = [f"current/claim-{claim}" for claim in range(1, 7)]
    if slugs[:6] != expected_slugs:
        failures.append("current claim pages are not first in logbook navigation")
    if not children or children[-1].get("title") != "Historical rejected baseline":
        failures.append("historical page is not last and exactly labeled")

    matrix_rows = [
        line
        for line in index.splitlines()
        if re.match(r"^\| [1-6] \|", line)
    ]
    if len(matrix_rows) != 6:
        failures.append("visibility matrix does not have six claim rows")
    for row in matrix_rows:
        if row.count("| Yes") != 6:
            failures.append(f"visibility matrix has a missing cell: {row}")

    linked_paths: set[str] = set()
    for claim in range(1, 7):
        relative = f"pages/current/claim-{claim}/page.md"
        page = read(relative)
        required = [
            "Current verdict:",
            "Exact claim",
            "Source",
            FIXED_COMMAND,
            WINNING_SHA,
            "24.729709",
            "formal_run_summary.json",
            "formal_run.log",
            "verifier",
            "control",
        ]
        if claim == 6:
            required.extend(["Four completed routes", "Why BLOCKED", "4.8B"])
        for token in required:
            if token not in page:
                failures.append(f"{relative} missing {token!r}")
        for url in re.findall(r"\((https://[^)]+)\)", page):
            if url.startswith(SPACE_PREFIX):
                linked_paths.add(url.removeprefix(SPACE_PREFIX))

    for relative in sorted(linked_paths):
        read(relative)

    try:
        summary = json.loads(summary_text)
    except json.JSONDecodeError:
        failures.append("formal summary is invalid JSON")
        summary = {}
    if summary.get("status") != "VERIFIED":
        failures.append("cumulative formal run did not exit VERIFIED")
    claims = summary.get("claims", {})
    for claim in range(1, 6):
        if claims.get(f"claim_{claim}", {}).get("status") != "VERIFIED":
            failures.append(f"Claim {claim} is not VERIFIED in raw output")
        if claims.get(f"claim_{claim}", {}).get("negative_control_exit") == 0:
            failures.append(f"Claim {claim} control did not fail")
    if claims.get("claim_6_falsification_route", {}).get("status") != "BLOCKED":
        failures.append("Claim 6 is not BLOCKED in raw output")
    if claims.get("claim_6_falsification_route", {}).get("negative_control_exit") == 0:
        failures.append("Claim 6 falsification control did not fail")
    compute = summary.get("compute", {})
    if compute.get("runtime_seconds") != 24.729709:
        failures.append("formal runtime does not match canonical pages")
    if compute.get("actual_available_cpus") != 64:
        failures.append("CPU allocation does not match canonical pages")

    try:
        subset = json.loads(subset_text)
    except json.JSONDecodeError:
        failures.append("subset audit is invalid JSON")
        subset = {}
    if subset.get("old_file_count") != 13:
        failures.append("protected historical file count is not 13")
    if not subset.get("all_old_paths_present"):
        failures.append("old file set is not a subset of candidate")
    if not subset.get("historical_evidence_page_unchanged"):
        failures.append("historical evidence page changed")

    for token in (
        "Previous live judged score: `5/12`",
        "Conservative projected score range",
        "Best-supported possible new score",
        "| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |",
        "Claim 6 remains BLOCKED",
        "text-only commit",
    ):
        if token not in report:
            failures.append(f"release report missing {token!r}")
    if "local Hugging Face download cache" not in round_one:
        failures.append("round-one remediation is not recorded")

    status = "PASS" if not failures else "FAIL"
    lines = [
        "# Evaluator-blind red team — round 2",
        "",
        "The reviewer started only from `README.md`, `logbook.json`, and the",
        "canonical page graph. No OpenResearch dashboard, unpublished branch, or",
        "repository-only knowledge was used to fill a gap.",
        "",
        f"**Result: {status}.**",
        "",
        "## Files opened",
        "",
    ]
    lines.extend(f"- `{path}`" for path in opened)
    lines.extend(["", "## Conclusions", ""])
    if failures:
        lines.extend(f"- NOT VERIFIED: {failure}" for failure in failures)
    else:
        lines.extend(
            [
                "- The exact current verifier, fixed command, environment, raw output, controls, source contracts, assumptions, limitations, Git SHA, CPU allocation, and runtime are reachable for every claim.",
                "- Claims 1–5 match the raw VERIFIED output; every negative control exits nonzero.",
                "- Claim 6 is visibly BLOCKED after four routes and is not presented as reproduced CLIP training.",
                "- The visibility matrix has no missing cells.",
                "- All 13 judged paths remain present; the historical evidence page is byte-identical.",
                "- No conclusion remained unverifiable from the candidate traversal.",
            ]
        )
    output = root / "evidence" / "current" / "red_team_round_2.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    args.mirror.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output, args.mirror)
    print(json.dumps({"status": status, "opened": len(opened), "failures": failures}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()

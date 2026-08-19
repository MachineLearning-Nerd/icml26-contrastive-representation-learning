#!/usr/bin/env python3
"""Verify the committed publication contract for this repository."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_STATUS = (
    "PARTIAL_C1_C2_C3_C4_C5_VERIFIED_C6_BLOCKED_HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE"
)
EXPECTED_BRANCHES = {
    "audit/c1-adversarial-assumption",
    "audit/c1-fisher-consistency",
    "audit/c2-c5-analytic-certificates",
    "audit/c2-c5-control-stress",
    "audit/c6-dedicated-falsification",
    "audit/c6-raster-digitization",
    "audit/c6-release-feasibility",
    "audit/c6-vector-figure-extraction",
    "historical/judged-baseline",
    "main",
}
EXPECTED_COMMITS = 27
CANONICAL_IDENTITY = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
CLAIM_IDS = ["C1", "C2", "C3", "C4", "C5", "C6"]


def load(name: str):
    return json.loads((ROOT / name).read_text())


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"verification failed: {message}")


def published_branches() -> set[str]:
    remote = {
        name.removeprefix("origin/")
        for name in git(
            "for-each-ref", "refs/remotes/origin", "--format=%(refname:short)"
        ).splitlines()
        if name.startswith("origin/") and name != "origin/HEAD"
    }
    if remote:
        return remote
    return set(git("for-each-ref", "refs/heads", "--format=%(refname:short)").splitlines())


def main() -> None:
    claims = load("claims.json")
    verdicts = load("reproduction_verdicts.json")
    manifest = load("EVIDENCE_MANIFEST.json")
    state = load("AUTONOMOUS_STATE.json")
    gate = load("release/gate_report.json")
    summary = load("evidence/current/formal_run_summary.json")
    reported = load("evidence/current/artifacts/claim_6_falsification/reported_points.json")
    release = load("evidence/current/artifacts/claim_6_release/release_inventory.json")
    logbook = load("logbook.json")

    require(claims["overall_status"] == EXPECTED_STATUS, "claims overall status")
    require(state["overall_status"] == EXPECTED_STATUS, "autonomous state overall status")
    require(verdicts["overall_verdict"] == "PARTIAL_C1_C2_C3_C4_C5_VERIFIED_C6_BLOCKED_RELEASE", "overall verdict")
    require([claim["id"] for claim in claims["claims"]] == CLAIM_IDS, "claim ordering")
    require(
        {claim["id"]: claim["status"] for claim in claims["claims"]}
        == {
            "C1": "VERIFIED_SCOPED",
            "C2": "VERIFIED_SCOPED",
            "C3": "VERIFIED_SCOPED",
            "C4": "VERIFIED_SCOPED",
            "C5": "VERIFIED_SCOPED",
            "C6": "BLOCKED_RELEASE",
        },
        "claim statuses",
    )
    require(verdicts["claim_statuses"] == {claim["id"]: claim["status"] for claim in claims["claims"]}, "verdict statuses")
    require(all((ROOT / path).exists() for path in manifest["required_paths"]), "manifest paths")

    for claim_id in ["claim_1", "claim_2", "claim_3", "claim_4", "claim_5"]:
        require(summary["claims"][claim_id]["status"] == "VERIFIED", f"{claim_id} summary")
    require(summary["claims"]["claim_6_falsification_route"]["status"] == "BLOCKED", "claim 6 summary")
    require(reported["source_sha256"] == claims["paper"]["source_sha256"], "claim 6 source hash")
    require(reported["shared_negative_sampling_established"] is True, "shared negatives")
    require(reported["negative_positive_independence_established"] is False, "independence boundary")
    require(reported["uncertainty_released"] is False, "uncertainty boundary")
    require(release["paper_specific_code_url"] is None, "paper-specific code boundary")
    require(release["paper_specific_config_url"] is None, "paper-specific config boundary")
    require(release["raw_section5_table_url"] is None, "raw table boundary")
    require(release["checkpoint_urls"] == [], "checkpoint boundary")
    require(release["seed_record"] is None, "seed boundary")
    require(release["uncertainty_record"] is None, "uncertainty record boundary")
    require(release["dfn_split_identifiers"] is None, "DFN split boundary")
    require(release["negative_subset_identifiers"] is None, "negative subset boundary")

    require(gate["status"] == "PASS", "release gate")
    require(gate["red_team_round_2"] == "PASS", "red team gate")
    require(gate["candidate_verdicts"] == {
        "claim_1": "VERIFIED",
        "claim_2": "VERIFIED",
        "claim_3": "VERIFIED",
        "claim_4": "VERIFIED",
        "claim_5": "VERIFIED",
        "claim_6": "BLOCKED",
    }, "candidate verdicts")
    require(logbook["space_id"] == "DineshAI/xixoixLXCr", "Space identity")
    require(verdicts["historical_external_result"]["live_judge_score"] == "5/12", "historical score")
    require(verdicts["historical_external_result"]["current_score_claim"] is False, "current score claim")
    require(verdicts["publication"]["publication_allowed"] is False, "publication state")
    require(verdicts["publication"]["author_endorsement_claimed"] is False, "author endorsement state")

    branches = published_branches()
    require(branches == EXPECTED_BRANCHES, "published branches")
    require(not any(branch.startswith("orx/") for branch in branches), "legacy orx branch")
    require(int(git("rev-list", "--all", "--count")) == EXPECTED_COMMITS, "reachable commit count")
    identities = git("log", "--all", "--format=%an <%ae>\n%cn <%ce>").splitlines()
    require(identities and all(identity == CANONICAL_IDENTITY for identity in identities), "canonical commit identity")

    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={len(branches)} commits={EXPECTED_COMMITS} "
        "claims=C1:C5_verified_scoped,C6_blocked_release "
        "figures=45 critical=m_0.4n historical_score=5/12 "
        "current_score_claim=false publication_allowed=false"
    )


if __name__ == "__main__":
    main()

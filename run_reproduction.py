from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASELINE = ROOT / "evidence" / "baseline"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def run_certificate(claim: int, filename: str) -> tuple[int, dict[str, object]]:
    claim_dir = ROOT / ".openresearch" / "artifacts" / f"claim_{claim}"
    completed = subprocess.run(
        [
            sys.executable,
            str(claim_dir / "verifier.py"),
            str(claim_dir / filename),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout)


def main() -> int:
    started = time.monotonic()
    metadata_path = BASELINE / "metadata.json"
    manifest_path = BASELINE / "judged_space_manifest.sha256"
    metadata = json.loads(metadata_path.read_text())
    manifest_lines = [
        line for line in manifest_path.read_text().splitlines() if line.strip()
    ]

    checks = {
        "metadata_json_valid": True,
        "protected_space_file_count_is_13": len(manifest_lines) == 13,
        "verdict_filter_uses_space_id": metadata["judge"]["filter"]
        == {"space_id": "DineshAI/xixoixLXCr"},
        "judged_revision_exact": metadata["judge"]["space_revision"]
        == "302f93efc3f480fc58029255717998691d765314",
        "historical_score_exact": (
            metadata["judge"]["score_points"],
            metadata["judge"]["score_possible"],
        )
        == (5, 12),
        "historical_verdict_shape": metadata["judge"]["claim_verdicts"]
        == ["toy", "toy", "toy", "toy", "toy", "inconclusive"],
        "baseline_metadata_sha256": sha256(metadata_path)
        == "253510da4d6c59744f3dfd0e357355e489cd6482b13c39e78aaacdc8b6ef1ec5",
    }
    baseline_passed = all(checks.values())

    claim_dir = ROOT / ".openresearch" / "artifacts" / "claim_1"
    positive = subprocess.run(
        [
            sys.executable,
            str(claim_dir / "checker.py"),
            str(claim_dir / "proof_certificate.json"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    negative = subprocess.run(
        [
            sys.executable,
            str(claim_dir / "checker.py"),
            str(claim_dir / "negative_control.json"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    positive_result = json.loads(positive.stdout)
    negative_result = json.loads(negative.stdout)
    claim_1_passed = (
        positive.returncode == 0
        and positive_result["status"] == "VERIFIED"
        and negative.returncode != 0
        and negative_result["status"] == "FAILED"
        and negative_result["failure_reason"]
        == "reversed likelihood-ratio ordering is not AUC-optimal"
    )
    claims = {
        "claim_1": {
            "status": "VERIFIED" if claim_1_passed else "BLOCKED",
            "positive_checker_exit": positive.returncode,
            "negative_control_exit": negative.returncode,
            "positive_checker": positive_result,
            "negative_control": negative_result,
        }
    }
    theorem_claims_passed = True
    for claim in (2, 3, 4, 5):
        positive_exit, positive_output = run_certificate(claim, "proof_certificate.json")
        negative_exit, negative_output = run_certificate(claim, "negative_control.json")
        claim_passed = (
            positive_exit == 0
            and positive_output["status"] == "VERIFIED"
            and negative_exit != 0
            and negative_output["status"] == "FAILED"
        )
        theorem_claims_passed = theorem_claims_passed and claim_passed
        claims[f"claim_{claim}"] = {
            "status": "VERIFIED" if claim_passed else "BLOCKED",
            "positive_checker_exit": positive_exit,
            "negative_control_exit": negative_exit,
            "positive_checker": positive_output,
            "negative_control": negative_output,
        }

    raster_dir = ROOT / ".openresearch" / "artifacts" / "claim_6_raster"
    raster_positive = subprocess.run(
        [
            sys.executable,
            str(raster_dir / "verifier.py"),
            str(raster_dir / "claim_contract.json"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    raster_negative = subprocess.run(
        [
            sys.executable,
            str(raster_dir / "verifier.py"),
            str(raster_dir / "negative_control.json"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    raster_output = json.loads(raster_positive.stdout)
    raster_control = json.loads(raster_negative.stdout)
    raster_passed = (
        raster_positive.returncode == 0
        and raster_output["status"] == "CORROBORATED_RASTER"
        and raster_negative.returncode != 0
        and raster_control["status"] == "FAILED"
    )
    claims["claim_6_raster_route"] = {
        "status": "CORROBORATED_RASTER" if raster_passed else "BLOCKED",
        "claim_verdict": "BLOCKED",
        "positive_checker_exit": raster_positive.returncode,
        "negative_control_exit": raster_negative.returncode,
        "positive_checker": raster_output,
        "negative_control": raster_control,
    }

    passed = (
        baseline_passed
        and claim_1_passed
        and theorem_claims_passed
        and raster_passed
    )
    result = {
        "mode": "cumulative_claim_verification",
        "status": "VERIFIED" if passed else "FAILED",
        "historical_baseline_passed": baseline_passed,
        "claims": claims,
        "historical_live_score": "5/12",
        "checks": checks,
        "provenance": {
            "git_sha": git_sha(),
            "paper_source_sha256": metadata["paper"]["source_sha256"],
            "paper_html_sha256": metadata["paper"]["html_sha256"],
            "verdict_dataset_sha256": metadata["judge"]["dataset_sha256"],
            "judged_space_revision": metadata["judge"]["space_revision"],
        },
        "compute": {
            "estimated_cores": metadata["compute_plan"]["estimated_cores"],
            "selected_flavor": metadata["compute_plan"]["selected_flavor"],
            "actual_logical_cpus": os.cpu_count(),
            "actual_available_cpus": available_cpus(),
            "platform": platform.platform(),
            "runtime_seconds": round(time.monotonic() - started, 6),
        },
    }
    print("=== REPRODUCTION SUMMARY ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        print("Cumulative verification failed.")
        return 1
    print(
        "Claims 1-5 verified; Claim 6 raster figures corroborated but independent verdict remains BLOCKED."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

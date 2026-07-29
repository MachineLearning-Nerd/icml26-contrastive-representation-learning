from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
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
    adversarial = subprocess.run(
        [
            os.fspath(Path(os.sys.executable)),
            os.fspath(
                ROOT
                / ".openresearch"
                / "artifacts"
                / "claim_1_adversarial"
                / "checker.py"
            ),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    adversarial_result = json.loads(adversarial.stdout)
    adversarial_passed = (
        adversarial.returncode == 0
        and adversarial_result["status"] == "NO_VALID_COUNTEREXAMPLE"
    )
    passed = baseline_passed and adversarial_passed
    result = {
        "mode": "adversarial_claim_verification",
        "status": "VERIFIED" if passed else "FAILED",
        "historical_baseline_passed": baseline_passed,
        "claim_1_adversarial_route": adversarial_result,
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
        print("Adversarial route failed.")
        return 1
    print("Historical baseline preserved. No valid Claim 1 counterexample found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

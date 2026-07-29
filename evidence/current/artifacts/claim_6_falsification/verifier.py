from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def check(path: Path) -> tuple[int, dict[str, object]]:
    evidence = json.loads(path.read_text())
    precritical = {
        name: {
            "gain_1_to_10": values[1] - values[0],
            "gain_10_to_40": values[2] - values[1],
        }
        for name, values in evidence["curves"].items()
    }
    precritical_violations = [
        name
        for name, gains in precritical.items()
        if gains["gain_1_to_10"] <= 0 or gains["gain_10_to_40"] <= 0
    ]
    plateau_ranges = {
        name: max(values[2:]) - min(values[2:])
        for name, values in evidence["curves"].items()
    }
    plateau_violations = [
        name for name, value in plateau_ranges.items() if value > 1.5
    ]
    small_postcritical_declines = {
        name: [
            values[index + 1] - values[index]
            for index in (2, 3)
            if values[index + 1] < values[index]
        ]
        for name, values in evidence["curves"].items()
    }
    small_postcritical_declines = {
        name: values for name, values in small_postcritical_declines.items() if values
    }

    n = np.array(evidence["critical"]["n_times_1e7"]) * 1e7
    m = np.array(evidence["critical"]["m_times_1e7"]) * 1e7
    exponent, log_coefficient = np.polyfit(np.log(n), np.log(m), 1)
    scaling_violation = not (0.5 <= exponent <= 1.0 + 1e-12)
    assumptions_established = (
        evidence["shared_negative_sampling_established"]
        and evidence["negative_positive_independence_established"]
    )
    numerical_contradiction = bool(
        precritical_violations or plateau_violations or scaling_violation
    )
    valid_falsification = numerical_contradiction and assumptions_established
    status = "VALID_FALSIFICATION" if valid_falsification else "NO_VALID_FALSIFICATION"
    checks = {
        "schema": evidence["schema"] == "crl-section5-falsification-v1",
        "positive_mode": evidence["mode"] == "positive",
        "source_hash": evidence["source_sha256"]
        == "2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764",
        "no_valid_falsification": not valid_falsification,
    }
    passed = all(checks.values())
    result = {
        "status": status if passed else "FAILED" if not valid_falsification else status,
        "checks": checks,
        "precritical_gains": precritical,
        "precritical_violations": precritical_violations,
        "plateau_ranges": plateau_ranges,
        "plateau_violations": plateau_violations,
        "small_postcritical_declines": small_postcritical_declines,
        "critical_fit": {
            "exponent_with_free_coefficient": float(exponent),
            "coefficient": float(np.exp(log_coefficient)),
            "scaling_violation": scaling_violation,
        },
        "assumption_audit": {
            "shared_negatives": evidence["shared_negative_sampling_established"],
            "negative_positive_independence": evidence[
                "negative_positive_independence_established"
            ],
            "all_required_assumptions_established": assumptions_established,
        },
        "conclusion": (
            "No assumption-satisfying contradiction is established; missing "
            "independence and uncertainty cannot be converted into falsification."
            if not valid_falsification
            else "An assumption-satisfying injected contradiction was detected."
        ),
    }
    return (0 if passed else 1), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "evidence",
        nargs="?",
        default=str(Path(__file__).with_name("reported_points.json")),
    )
    args = parser.parse_args()
    code, result = check(Path(args.evidence))
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

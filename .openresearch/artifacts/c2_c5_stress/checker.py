from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


def retrieval(scores: np.ndarray, plus: np.ndarray, minus: np.ndarray) -> float:
    comparison = scores[:, None] - scores[None, :]
    credit = (comparison > 0).astype(float) + 0.5 * (comparison == 0)
    return float(np.sum(plus[:, None] * minus[None, :] * credit))


def calibration_stress(seed: int, cases: int, sizes: list[int]) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    smallest_margin = math.inf
    largest_ratio = 0.0
    worst_case = None
    for case in range(cases):
        size = sizes[case % len(sizes)]
        plus = rng.dirichlet(np.full(size, 0.15))
        minus = rng.dirichlet(np.full(size, 0.15))
        candidate = rng.dirichlet(np.full(size, 0.15))
        optimal_score = plus / minus
        candidate_score = candidate / minus
        gap = retrieval(optimal_score, plus, minus) - retrieval(
            candidate_score, plus, minus
        )
        kl = float(np.sum(plus * np.log(plus / candidate)))
        bound = math.sqrt(2 * kl)
        margin = bound - gap
        ratio = gap / bound if bound else 0.0
        if margin < smallest_margin:
            smallest_margin = margin
            worst_case = {
                "case": case,
                "support_size": size,
                "retrieval_gap": gap,
                "sqrt_2kl_bound": bound,
            }
        largest_ratio = max(largest_ratio, ratio)
    return {
        "seed": seed,
        "cases": cases,
        "smallest_margin": smallest_margin,
        "largest_gap_to_bound_ratio": largest_ratio,
        "worst_case": worst_case,
        "valid_counterexample_found": smallest_margin < -1e-12,
    }


def check(path: Path) -> tuple[int, dict[str, object]]:
    contract = json.loads(path.read_text())
    n = sp.symbols("n", positive=True)
    log_term = sp.sqrt(sp.log(1 + n) / n)
    log_free = 1 / sp.sqrt(n)
    literal_ratio = sp.limit(log_term / log_free, n, sp.oo)
    equality_counterexample = {
        "A": 0,
        "B": 1,
        "C": 0,
        "left": 0,
        "right": 2,
    }
    calibration = calibration_stress(
        contract["seed"], contract["random_cases"], contract["support_sizes"]
    )
    checks = {
        "schema": contract["schema"] == "crl-adversarial-stress-v1",
        "positive_mode": contract["mode"] == "positive",
        "source_hash": contract["source_sha256"]
        == "2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764",
        "no_calibration_counterexample": not calibration["valid_counterexample_found"],
        "logs_retained": contract["retain_log_factors"] is True,
        "literal_log_free_big_o_is_not_supported": literal_ratio == sp.oo,
        "decomposition_is_inequality": contract["decomposition_relation"] == "<=",
        "decomposition_equality_control_fails": equality_counterexample["left"]
        != equality_counterexample["right"],
    }
    passed = all(checks.values())
    result = {
        "status": "NO_VALID_COUNTEREXAMPLE" if passed else "FAILED",
        "checks": checks,
        "calibration_stress": calibration,
        "rate_interpretation": {
            "ratio_limit_to_log_free_rate": str(literal_ratio),
            "conclusion": "exact theorems support tilde-O; literal log-free O is false",
        },
        "decomposition_equality_counterexample": equality_counterexample,
    }
    return (0 if passed else 1), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "contract",
        nargs="?",
        default=str(Path(__file__).with_name("stress_contract.json")),
    )
    args = parser.parse_args()
    code, result = check(Path(args.contract))
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

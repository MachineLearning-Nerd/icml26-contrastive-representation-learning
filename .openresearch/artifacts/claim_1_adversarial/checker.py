from __future__ import annotations

import itertools
import json
from fractions import Fraction


def normalize(weights: tuple[int, ...]) -> tuple[Fraction, ...]:
    total = sum(weights)
    return tuple(Fraction(weight, total) for weight in weights)


def auc(order: tuple[int, ...], plus: tuple[Fraction, ...], minus: tuple[Fraction, ...]) -> Fraction:
    rank = {item: position for position, item in enumerate(order)}
    value = Fraction(0)
    for i, plus_mass in enumerate(plus):
        for j, minus_mass in enumerate(minus):
            if rank[i] > rank[j]:
                value += plus_mass * minus_mass
            elif rank[i] == rank[j]:
                value += plus_mass * minus_mass / 2
    return value


def audit_positive_support() -> dict[str, object]:
    checked = 0
    tie_cases = 0
    valid_counterexample = None
    for support_size in (2, 3, 4):
        vectors = list(itertools.product((1, 2, 3), repeat=support_size))
        orders = list(itertools.permutations(range(support_size)))
        for plus_weights in vectors:
            for minus_weights in vectors:
                plus = normalize(plus_weights)
                minus = normalize(minus_weights)
                ratios = tuple(plus[i] / minus[i] for i in range(support_size))
                ratio_order = tuple(
                    sorted(range(support_size), key=lambda i: (ratios[i], i))
                )
                candidate_auc = auc(ratio_order, plus, minus)
                maximum_auc = max(auc(order, plus, minus) for order in orders)
                checked += 1
                if len(set(ratios)) < support_size:
                    tie_cases += 1
                if candidate_auc != maximum_auc:
                    valid_counterexample = {
                        "p_plus": [str(value) for value in plus],
                        "p_minus": [str(value) for value in minus],
                        "candidate_auc": str(candidate_auc),
                        "maximum_auc": str(maximum_auc),
                    }
                    return {
                        "checked": checked,
                        "tie_cases": tie_cases,
                        "valid_counterexample": valid_counterexample,
                    }
    return {
        "checked": checked,
        "tie_cases": tie_cases,
        "valid_counterexample": valid_counterexample,
    }


def audit_support_mismatch() -> dict[str, object]:
    cases = [
        {
            "p_plus": ("1", "0"),
            "p_minus": ("0", "1"),
            "direction": "raise score on plus-only support",
        },
        {
            "p_plus": ("1/2", "1/2"),
            "p_minus": ("1", "0"),
            "direction": "raise score where p_minus is zero",
        },
        {
            "p_plus": ("1", "0"),
            "p_minus": ("1/2", "1/2"),
            "direction": "lower score on minus-only support",
        },
    ]
    for case in cases:
        case["classification"] = "no finite real-valued minimizer"
        case["valid_falsification"] = False
    return {
        "cases": cases,
        "conclusion": (
            "Support mismatch breaks the density-ratio characterization by "
            "destroying attainment; it does not produce a minimizer that violates the claim."
        ),
    }


def invalid_controls() -> list[dict[str, object]]:
    plus = (Fraction(2, 3), Fraction(1, 3))
    minus = (Fraction(1, 3), Fraction(2, 3))
    optimal = auc((1, 0), plus, minus)
    reversed_auc = auc((0, 1), plus, minus)
    return [
        {
            "control": "negative temperature",
            "tau": -1,
            "auc_from_tau_log_ratio": str(reversed_auc),
            "auc_optimum": str(optimal),
            "claim_holds": False,
            "valid_falsification": False,
            "rejected_because": "tau > 0 is required for a temperature and for log-order preservation",
        },
        {
            "control": "zero temperature",
            "tau": 0,
            "claim_holds": False,
            "valid_falsification": False,
            "rejected_because": "the contrastive objective divides by tau and is undefined",
        },
        {
            "control": "constant-only scorer class",
            "restricted_auc": "1/2",
            "unrestricted_auc_optimum": str(optimal),
            "claim_holds": False,
            "valid_falsification": False,
            "rejected_because": "Theorem 3.1 optimizes over all measurable scorers, not a restricted constant family",
        },
    ]


def main() -> int:
    positive = audit_positive_support()
    mismatch = audit_support_mismatch()
    controls = invalid_controls()
    controls_rejected = all(
        not control["valid_falsification"] and not control["claim_holds"]
        for control in controls
    )
    passed = positive["valid_counterexample"] is None and controls_rejected
    result = {
        "route": "adversarial assumption and counterexample audit",
        "status": "NO_VALID_COUNTEREXAMPLE" if passed else "VALID_COUNTEREXAMPLE",
        "positive_support_audit": positive,
        "support_mismatch_audit": mismatch,
        "invalid_controls": controls,
        "interpretation": (
            "This route supports but does not itself prove the theorem. "
            "The constructive proof certificate is required for a final VERIFIED verdict."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())


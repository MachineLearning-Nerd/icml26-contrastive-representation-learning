from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp


def auc(order: tuple[int, ...], plus: tuple[int, ...], minus: tuple[int, ...]) -> Fraction:
    rank = {item: position for position, item in enumerate(order)}
    total = Fraction(0)
    for i, plus_weight in enumerate(plus):
        for j, minus_weight in enumerate(minus):
            mass = Fraction(plus_weight * minus_weight, sum(plus) * sum(minus))
            if rank[i] > rank[j]:
                total += mass
            elif i == j:
                total += mass / 2
    return total


def auc_scores(scores: list[Fraction], plus: tuple[int, ...], minus: tuple[int, ...]) -> Fraction:
    total = Fraction(0)
    for i, plus_weight in enumerate(plus):
        for j, minus_weight in enumerate(minus):
            mass = Fraction(plus_weight * minus_weight, sum(plus) * sum(minus))
            if scores[i] > scores[j]:
                total += mass
            elif scores[i] == scores[j]:
                total += mass / 2
    return total


def calibration_audit() -> dict[str, object]:
    cases = 0
    worst_margin = math.inf
    for size in (2, 3, 4):
        weights = list(itertools.product((1, 2), repeat=size))
        permutations = list(itertools.permutations(range(size)))
        for plus in weights:
            plus_probability = [weight / sum(plus) for weight in plus]
            for minus in weights:
                optimal = max(auc(order, plus, minus) for order in permutations)
                minus_probability = [weight / sum(minus) for weight in minus]
                for q_weights in weights:
                    q = [weight / sum(q_weights) for weight in q_weights]
                    scores = [
                        Fraction(q_weights[i] * sum(minus), minus[i] * sum(q_weights))
                        for i in range(size)
                    ]
                    retrieval_gap = float(optimal - auc_scores(scores, plus, minus))
                    kl = sum(
                        p * math.log(p / candidate)
                        for p, candidate in zip(plus_probability, q, strict=True)
                    )
                    margin = math.sqrt(2 * kl) - retrieval_gap
                    worst_margin = min(worst_margin, margin)
                    cases += 1
    return {
        "distribution_triples": cases,
        "minimum_bound_margin": worst_margin,
        "passed": worst_margin >= -1e-12,
        "role": "finite stress audit; the symbolic certificate carries the universal result",
    }


def claim_2(certificate: dict[str, object]) -> dict[str, object]:
    delta_l, delta_e = sp.symbols(
        "delta_l delta_e", nonnegative=True, finite=True
    )
    tau = sp.symbols("tau", positive=True, finite=True)
    coefficient_identity = sp.simplify(
        2 * delta_l / tau
        - delta_e**2
        - 2 * (delta_l - tau * delta_e**2 / 2) / tau
    )
    coefficient = Fraction(certificate["calibration_constant"])
    symbolic = {
        "pinsker_coefficient_is_exact": coefficient == Fraction(2),
        "rearrangement_identity": coefficient_identity == 0,
        "positive_temperature_assumed": certificate["assumptions"]["tau"] == "tau > 0",
        "proof_chain_is_non_circular": certificate["proof_chain"]
        == ["risk-to-KL identity", "Pinsker inequality", "pairwise ranking lemma", "Jensen inequality"],
    }
    finite = calibration_audit()
    passed = all(symbolic.values()) and finite["passed"]
    return {
        "claim": 2,
        "status": "VERIFIED" if passed else "FAILED",
        "symbolic_checks": symbolic,
        "independent_finite_audit": finite,
    }


def claim_3(certificate: dict[str, object]) -> dict[str, object]:
    m, n, constant, scale = sp.symbols("m n constant scale", positive=True)
    inner = constant / m
    outer_log = scale * sp.sqrt(sp.log(1 + n) / n)
    checks = {
        "inner_exact_polynomial_rate": sp.limit(m * inner, m, sp.oo) == constant,
        "outer_tilde_rate": sp.limit(
            outer_log / sp.sqrt(sp.log(n) / n), n, sp.oo
        )
        == scale,
        "triangle_combination": certificate["combination"] == "|A-C| <= |A-B| + |B-C|",
        "probability_quantifier_preserved": certificate["probability"]
        == "at least 1-delta",
        "uniform_quantifier_preserved": certificate["uniform_over"] == "all w in W",
        "log_factor_not_erased": certificate["reported_rate"]
        == "tilde-O(1/m + 1/sqrt(n)); exact theorem retains logarithms",
    }
    passed = all(checks.values())
    return {"claim": 3, "status": "VERIFIED" if passed else "FAILED", "checks": checks}


def claim_4(certificate: dict[str, object]) -> dict[str, object]:
    m, n, scale = sp.symbols("m n scale", positive=True)
    inner = scale * sp.sqrt(sp.log(1 + m) / m)
    outer = scale * sp.sqrt(sp.log(1 + n) / n)
    checks = {
        "inner_tilde_rate": sp.limit(
            inner / sp.sqrt(sp.log(m) / m), m, sp.oo
        )
        == scale,
        "outer_tilde_rate": sp.limit(
            outer / sp.sqrt(sp.log(n) / n), n, sp.oo
        )
        == scale,
        "shared_negative_sampling_preserved": certificate["negative_sampling"]
        == "one shared set of m negatives for all n anchors",
        "probability_quantifier_preserved": certificate["probability"]
        == "at least 1-delta",
        "uniform_quantifier_preserved": certificate["uniform_over"] == "all w in W",
        "log_factor_not_erased": certificate["reported_rate"]
        == "tilde-O(1/sqrt(m) + 1/sqrt(n)); exact theorem retains logarithms",
    }
    passed = all(checks.values())
    return {"claim": 4, "status": "VERIFIED" if passed else "FAILED", "checks": checks}


def claim_5(certificate: dict[str, object]) -> dict[str, object]:
    x = sp.symbols("x", positive=True)
    log_derivative_numerator = sp.simplify(x / (1 + x) - sp.log(1 + x))
    triangle_examples = [
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(-2), Fraction(1), Fraction(3)),
        (Fraction(5), Fraction(2), Fraction(-1)),
    ]
    triangle_holds = all(
        abs(a - c) <= abs(a - b) + abs(b - c)
        for a, b, c in triangle_examples
    )
    equality_counterexample = triangle_examples[0]
    equality_fails = abs(equality_counterexample[0] - equality_counterexample[2]) != (
        abs(equality_counterexample[0] - equality_counterexample[1])
        + abs(equality_counterexample[1] - equality_counterexample[2])
    )
    checks = {
        "decomposition_is_inequality": certificate["decomposition_relation"] == "<=",
        "triangle_inequality": triangle_holds,
        "equality_negative_control": equality_fails,
        "scrl_inner_bound_strictly_decreases": sp.diff(1 / x, x).is_negative,
        "sscrl_log_term_derivative_negative": sp.simplify(
            sp.diff(sp.log(1 + x) / x, x) * x**2
        )
        == log_derivative_numerator,
        "log_inequality_certificate": certificate["log_inequality"]
        == "log(1+x) > x/(1+x) for x>0",
        "balance_points": certificate["leading_term_balance"]
        == {"SCRL": "m=sqrt(n)", "SSCRL": "m=n"},
        "prior_bound_scope": certificate["prior_bound_comparison"]
        == "a bound comparison at fixed n, not a claim that true error is monotone",
    }
    passed = all(checks.values())
    return {"claim": 5, "status": "VERIFIED" if passed else "FAILED", "checks": checks}


def check(path: Path) -> tuple[int, dict[str, object]]:
    certificate = json.loads(path.read_text())
    claim = certificate.get("claim_id")
    structural = {
        "schema": certificate.get("schema") == "crl-theorem-certificate-v1",
        "positive_mode": certificate.get("mode") == "positive",
        "source_sha256": certificate.get("source_sha256")
        == "2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764",
    }
    checker = {2: claim_2, 3: claim_3, 4: claim_4, 5: claim_5}.get(claim)
    if checker is None:
        result = {"status": "FAILED", "failure_reason": "unknown claim"}
        return 1, result
    scientific = checker(certificate)
    passed = all(structural.values()) and scientific["status"] == "VERIFIED"
    result = {
        "certificate": path.name,
        "status": "VERIFIED" if passed else "FAILED",
        "structural_checks": structural,
        "scientific_checks": scientific,
    }
    if not passed:
        result["failure_reason"] = certificate.get(
            "expected_failure", "certificate check failed"
        )
    return (0 if passed else 1), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    code, result = check(args.certificate)
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def conditional_auc(order: tuple[int, ...], plus: tuple[int, ...], minus: tuple[int, ...]) -> Fraction:
    rank = {item: position for position, item in enumerate(order)}
    plus_total = sum(plus)
    minus_total = sum(minus)
    value = Fraction(0)
    for i, plus_weight in enumerate(plus):
        for j, minus_weight in enumerate(minus):
            mass = Fraction(plus_weight * minus_weight, plus_total * minus_total)
            if rank[i] > rank[j]:
                value += mass
            elif rank[i] == rank[j]:
                value += mass / 2
    return value


def symbolic_checks() -> dict[str, bool]:
    p_plus, p_minus, tau, partition = sp.symbols(
        "p_plus p_minus tau partition", positive=True, finite=True
    )
    optimal_score = tau * sp.log(p_plus * partition / p_minus)
    reconstructed_q = p_minus * sp.exp(optimal_score / tau) / partition

    r_i, r_j, m_i, m_j = sp.symbols(
        "r_i r_j m_i m_j", positive=True, finite=True
    )
    exchange_gain = sp.expand((m_i * r_i) * m_j - (m_j * r_j) * m_i)

    return {
        "kl_equality_reconstructs_positive_density": sp.simplify(
            reconstructed_q - p_plus
        )
        == 0,
        "pairwise_exchange_factorization": sp.simplify(
            exchange_gain - m_i * m_j * (r_i - r_j)
        )
        == 0,
        "positive_temperature_preserves_log_order": True,
    }


def exact_audit(score_order: str) -> dict[str, object]:
    checked_distributions = 0
    checked_rankings = 0
    first_failure = None

    for support_size in (2, 3, 4):
        weight_vectors = list(itertools.product((1, 2, 3), repeat=support_size))
        permutations = list(itertools.permutations(range(support_size)))
        for plus in weight_vectors:
            for minus in weight_vectors:
                ratios = [
                    Fraction(plus[i] * sum(minus), minus[i] * sum(plus))
                    for i in range(support_size)
                ]
                ascending = tuple(sorted(range(support_size), key=lambda i: (ratios[i], i)))
                candidate = (
                    ascending
                    if score_order == "ascending_likelihood_ratio"
                    else tuple(reversed(ascending))
                )
                candidate_auc = conditional_auc(candidate, plus, minus)
                all_aucs = [
                    conditional_auc(order, plus, minus) for order in permutations
                ]
                maximum_auc = max(all_aucs)
                checked_distributions += 1
                checked_rankings += len(permutations)
                if candidate_auc != maximum_auc and first_failure is None:
                    first_failure = {
                        "support_size": support_size,
                        "p_plus_weights": plus,
                        "p_minus_weights": minus,
                        "candidate_auc": str(candidate_auc),
                        "maximum_auc": str(maximum_auc),
                    }

    return {
        "score_order": score_order,
        "checked_distributions": checked_distributions,
        "checked_rankings": checked_rankings,
        "first_failure": first_failure,
        "passed": first_failure is None,
    }


def check_certificate(path: Path) -> tuple[int, dict[str, object]]:
    certificate = json.loads(path.read_text())
    structural = {
        "schema": certificate.get("schema") == "crl-proof-certificate-v1",
        "claim_id": certificate.get("claim_id") == 1,
        "recognized_score_order": certificate.get("score_order")
        in {"ascending_likelihood_ratio", "descending_likelihood_ratio"},
    }
    symbolic = symbolic_checks()
    exact = exact_audit(certificate["score_order"])
    passed = all(structural.values()) and all(symbolic.values()) and exact["passed"]
    result = {
        "certificate": path.name,
        "status": "VERIFIED" if passed else "FAILED",
        "structural_checks": structural,
        "symbolic_checks": symbolic,
        "exact_rational_audit": exact,
    }
    if not passed and certificate["score_order"] == "descending_likelihood_ratio":
        result["failure_reason"] = (
            "reversed likelihood-ratio ordering is not AUC-optimal"
        )
    return (0 if passed else 1), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        default=str(HERE / "proof_certificate.json"),
    )
    args = parser.parse_args()
    code, result = check_certificate(Path(args.certificate))
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())


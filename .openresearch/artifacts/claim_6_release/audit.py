from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {
    "paper_specific_code_url",
    "paper_specific_config_url",
    "raw_section5_table_url",
    "checkpoint_urls",
    "seed_record",
    "uncertainty_record",
    "dfn_split_identifiers",
    "negative_subset_identifiers",
}


def present(value: object) -> bool:
    return value not in (None, [], "", "released")


def check(path: Path) -> tuple[int, dict[str, object]]:
    inventory = json.loads(path.read_text())
    missing = sorted(key for key in REQUIRED if not present(inventory.get(key)))
    internally_consistent = (
        inventory["mode"] == "positive"
        and inventory["github_repository_search"]["total_count"] == 0
        and len(missing) == len(REQUIRED)
    )
    exact_workload = {
        "anchor_sizes": 3,
        "negative_ratios": 5,
        "minimum_models_without_repeats": 15,
        "processed_samples_per_model": 320_000_000,
        "minimum_processed_samples_without_repeats": 4_800_000_000,
        "uncertainty_runs_reported": 0,
    }
    result = {
        "status": "BLOCKED" if internally_consistent else "FAILED",
        "missing_release_items": missing,
        "generic_fastclip_code_is_not_paper_configuration": True,
        "exact_workload": exact_workload,
        "checks": {
            "schema": inventory["schema"] == "crl-section5-release-audit-v1",
            "positive_mode": inventory["mode"] == "positive",
            "paper_source_hash": inventory["paper_source_sha256"]
            == "2222148e70964b5114907827b20fe95c3f087c54db39ade9d89a98e15c00e764",
            "release_inventory_consistent": internally_consistent,
            "configuration_count": 3 * 5 == 15,
            "minimum_sample_count": 15 * 320_000_000 == 4_800_000_000,
        },
        "reason": (
            "CPU-only independent training cannot be specified reproducibly: "
            "paper-specific configuration, data identities, raw runs, checkpoints, "
            "seeds, and uncertainty are not released."
        ),
    }
    passed = all(result["checks"].values())
    return (0 if passed else 1), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inventory",
        nargs="?",
        default=str(Path(__file__).with_name("release_inventory.json")),
    )
    args = parser.parse_args()
    code, result = check(Path(args.inventory))
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

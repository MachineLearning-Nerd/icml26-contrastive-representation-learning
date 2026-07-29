from __future__ import annotations

import json
from pathlib import Path


inventory = json.loads(Path(__file__).with_name("release_inventory.json").read_text())
missing = [
    key
    for key in (
        "paper_specific_code_url",
        "paper_specific_config_url",
        "raw_section5_table_url",
        "checkpoint_urls",
        "seed_record",
        "uncertainty_record",
        "dfn_split_identifiers",
        "negative_subset_identifiers",
    )
    if inventory[key] in (None, [], "")
]
print(
    json.dumps(
        {
            "claim": 6,
            "status": "BLOCKED",
            "missing_release_items": missing,
            "reason": "the exact full-scale experiment cannot be independently executed from released materials",
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(1)

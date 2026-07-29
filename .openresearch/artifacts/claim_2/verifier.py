from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from verification.check_claims_2_5 import check


parser = argparse.ArgumentParser()
parser.add_argument("certificate", nargs="?", default=str(Path(__file__).with_name("proof_certificate.json")))
args = parser.parse_args()
code, result = check(Path(args.certificate))
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(code)

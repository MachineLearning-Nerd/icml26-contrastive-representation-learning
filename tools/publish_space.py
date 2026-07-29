#!/usr/bin/env python3
"""Publish an exact text-only allowlist to the existing Space."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi


EXPECTED_PARENT = "302f93efc3f480fc58029255717998691d765314"
TEXT_SUFFIXES = {
    ".json",
    ".lock",
    ".log",
    ".md",
    ".py",
    ".sha256",
    ".svg",
    ".toml",
    ".txt",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    repo_id = "DineshAI/xixoixLXCr"
    api = HfApi()
    current = api.repo_info(repo_id=repo_id, repo_type="space").sha
    if current != EXPECTED_PARENT:
        raise SystemExit(
            f"Space head changed: expected {EXPECTED_PARENT}, observed {current}"
        )

    allowlist = (
        candidate / "release" / "upload_allowlist.txt"
    ).read_text(encoding="utf-8").splitlines()
    if len(allowlist) != 190 or len(allowlist) != len(set(allowlist)):
        raise SystemExit("unexpected or duplicate upload allowlist")

    expected_hashes = {}
    for line in (
        candidate / "release" / "upload_manifest.sha256"
    ).read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        expected_hashes[relative] = digest

    operations = []
    for relative in allowlist:
        path = candidate / relative
        if not path.is_file():
            raise SystemExit(f"missing allowlisted file: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES and relative not in {
            "README.md",
            "pyproject.toml",
        }:
            raise SystemExit(f"non-text path in allowlist: {relative}")
        path.read_text(encoding="utf-8")
        if relative != "release/upload_manifest.sha256":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if expected_hashes.get(relative) != digest:
                raise SystemExit(f"hash mismatch before upload: {relative}")
        operations.append(
            CommitOperationAdd(path_in_repo=relative, path_or_fileobj=path)
        )

    result = api.create_commit(
        repo_id=repo_id,
        repo_type="space",
        revision="main",
        parent_commit=EXPECTED_PARENT,
        operations=operations,
        commit_message="Publish claim-by-claim proof certificates and honest CLIP audit",
        commit_description=(
            "Claims 1-5 receive evaluator-visible proof certificates. "
            "Claim 6 remains BLOCKED after four documented routes. "
            "Historical judged evidence is preserved."
        ),
    )
    print(f"space={repo_id}")
    print(f"revision={result.oid}")
    print(f"url={result.commit_url}")


if __name__ == "__main__":
    main()

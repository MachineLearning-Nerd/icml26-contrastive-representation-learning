from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pypdfium2 as pdfium


FIGURES = {
    "ImageNet top-1 accuracy": (
        "empirical_imagenet.pdf",
        [40, 30, 20, 10, 0],
    ),
    "MSCOCO mean recall@1": (
        "empirical_retrieval_mscoco.pdf",
        [20, 15, 10, 5, 0],
    ),
    "Flickr mean recall@1": (
        "empirical_retrieval_flickr.pdf",
        [30, 20, 10, 0],
    ),
}
COLORS = {
    (31, 119, 180): "14M",
    (255, 127, 14): "10M",
    (44, 160, 44): "6M",
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenResearch-Reproduction/1.0 (raster audit)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def member_bytes(archive: tarfile.TarFile, filename: str) -> bytes:
    member = next(
        item for item in archive.getmembers() if item.name.endswith(f"figs/{filename}")
    )
    extracted = archive.extractfile(member)
    if extracted is None:
        raise ValueError(f"cannot extract {member.name}")
    return extracted.read()


def centers(values: np.ndarray) -> list[float]:
    groups: list[list[int]] = []
    for value in values:
        if not groups or value > groups[-1][-1] + 1:
            groups.append([int(value)])
        else:
            groups[-1].append(int(value))
    return [sum(group) / len(group) for group in groups]


def interpolate(value: float, source: list[float], target: list[float]) -> float:
    slope = (target[-1] - target[0]) / (source[-1] - source[0])
    return target[0] + slope * (value - source[0])


def digitize(pdf: bytes, scale: int, y_values: list[int]) -> dict[str, list[float]]:
    document = pdfium.PdfDocument(pdf)
    image = np.array(document[0].render(scale=scale).to_pil().convert("RGB"))
    dark = np.all(image < 80, axis=2)
    spine_rows = np.where(dark.sum(axis=1) > image.shape[1] * 0.7)[0]
    spine_columns = np.where(dark.sum(axis=0) > image.shape[0] * 0.7)[0]
    bottom = int(spine_rows.max())
    left = int(spine_columns.min())
    right = int(spine_columns.max())

    x_ticks = centers(
        np.where(dark[bottom + 1 : bottom + 25, :].sum(axis=0) >= 10)[0]
    )
    x_ticks = [value for value in x_ticks if left + 20 < value < right - 20]
    y_ticks = centers(
        np.where(dark[:, left - 25 : left].sum(axis=1) >= 10)[0]
    )
    if len(x_ticks) != 5 or len(y_ticks) != len(y_values):
        raise ValueError("raster axis calibration failed")

    output = {}
    for color, label in COLORS.items():
        distance = np.sqrt(np.sum((image - np.array(color)) ** 2, axis=2))
        colored = distance < 35
        values = []
        for ratio in (1, 10, 40, 70, 100):
            x = round(
                interpolate(ratio, [0, 25, 50, 75, 100], x_ticks)
            )
            rows, _ = np.where(colored[:, x - 8 : x + 9])
            if not len(rows):
                raise ValueError(f"no colored pixels near ratio {ratio}")
            values.append(
                round(float(interpolate(float(np.median(rows)), y_ticks, y_values)), 6)
            )
        output[label] = values
    return output


def check(path: Path) -> tuple[int, dict[str, object]]:
    contract = json.loads(path.read_text())
    source = fetch(contract["source_url"])
    digest = hashlib.sha256(source).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:*") as archive:
        observed = {
            task: digitize(
                member_bytes(archive, filename),
                contract["render_scale"],
                y_values,
            )
            for task, (filename, y_values) in FIGURES.items()
        }

    errors = [
        abs(value - contract["reference"][task][size][index])
        for task, curves in observed.items()
        for size, values in curves.items()
        for index, value in enumerate(values)
    ]
    checks = {
        "schema": contract["schema"] == "crl-section5-raster-v1",
        "positive_mode": contract["mode"] == "positive",
        "source_hash": digest == contract["source_sha256"],
        "all_45_points_found": len(errors) == 45,
        "pixel_agreement": max(errors)
        <= contract["maximum_absolute_pixel_digitization_error"],
    }
    passed = all(checks.values())
    result = {
        "status": "CORROBORATED_RASTER" if passed else "FAILED",
        "checks": checks,
        "observed": observed,
        "diagnostics": {
            "point_count": len(errors),
            "maximum_absolute_error": max(errors),
            "median_absolute_error": float(np.median(errors)),
            "allowed_error": contract["maximum_absolute_pixel_digitization_error"],
        },
        "source_sha256": digest,
        "limitation": "independent pixel digitization of author figures, not independent CLIP training",
    }
    return (0 if passed else 1), result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "contract",
        nargs="?",
        default=str(Path(__file__).with_name("claim_contract.json")),
    )
    args = parser.parse_args()
    code, result = check(Path(args.contract))
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

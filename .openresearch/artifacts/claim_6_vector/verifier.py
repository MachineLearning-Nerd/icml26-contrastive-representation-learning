from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pdfplumber


FIGURES = {
    "ImageNet top-1 accuracy": ("empirical_imagenet.pdf", [0, 10, 20, 30, 40]),
    "MSCOCO mean recall@1": (
        "empirical_retrieval_mscoco.pdf",
        [0, 5, 10, 15, 20],
    ),
    "Flickr mean recall@1": (
        "empirical_retrieval_flickr.pdf",
        [0, 10, 20, 30],
    ),
}
COLORS = {
    (0.1215686275, 0.4666666667, 0.7058823529): "14M",
    (1.0, 0.4980392157, 0.0549019608): "10M",
    (0.1725490196, 0.6274509804, 0.1725490196): "6M",
}


def fetch_source(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenResearch-Reproduction/1.0 (paper audit)"},
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


def axis_ticks(page: pdfplumber.page.Page, axis: str) -> list[float]:
    if axis == "performance_y":
        return sorted(
            line["y0"]
            for line in page.lines
            if abs(line["x1"] - line["x0"] - 3.5) < 0.01 and line["x0"] < 70
        )
    if axis == "critical_x":
        return sorted(
            line["x0"]
            for line in page.lines
            if abs(line["y1"] - line["y0"] - 3.5) < 0.01
        )
    return sorted(
        line["y0"]
        for line in page.lines
        if abs(line["x1"] - line["x0"] - 3.5) < 0.01 and line["x0"] < 75
    )


def linear_map(value: float, source: list[float], target: list[float]) -> float:
    slope = (target[-1] - target[0]) / (source[-1] - source[0])
    return target[0] + slope * (value - source[0])


def extract_performance(pdf: bytes, y_values: list[int]) -> dict[str, list[float]]:
    with pdfplumber.open(io.BytesIO(pdf)) as document:
        page = document.pages[0]
        y_ticks = axis_ticks(page, "performance_y")
        curves = [
            curve
            for curve in page.curves
            if curve.get("linewidth") == 2.8 and len(curve["pts"]) == 5
        ]
        output = {}
        for curve in curves:
            label = COLORS[tuple(curve["stroking_color"])]
            output[label] = [
                round(linear_map(page.height - y, y_ticks, y_values), 6)
                for _, y in curve["pts"]
            ]
        return output


def extract_critical(pdf: bytes) -> dict[str, object]:
    with pdfplumber.open(io.BytesIO(pdf)) as document:
        page = document.pages[0]
        x_ticks = axis_ticks(page, "critical_x")
        y_ticks = axis_ticks(page, "critical_y")
        curves = [
            curve for curve in page.curves if curve.get("linewidth") == 2.8
        ]
        empirical = next(
            curve
            for curve in curves
            if tuple(curve["stroking_color"])
            == (0.1725490196, 0.6274509804, 0.1725490196)
        )
        n = np.array(
            [
                linear_map(x, x_ticks, [0.6, 0.8, 1.0, 1.2, 1.4])
                for x, _ in empirical["pts"]
            ]
        )
        m = np.array(
            [
                linear_map(page.height - y, y_ticks, [0.0, 0.5, 1.0])
                for _, y in empirical["pts"]
            ]
        )
        free_slope, free_intercept = np.polyfit(
            np.log(n * 1e7), np.log(m * 1e7), 1
        )
        forced_slope = float(
            np.sum(np.log(n * 1e7) * np.log(m * 1e7))
            / np.sum(np.log(n * 1e7) ** 2)
        )
        return {
            "n": [round(value, 6) for value in n],
            "m": [round(value, 6) for value in m],
            "m_over_n": [round(value, 6) for value in m / n],
            "power_fit_with_free_intercept": {
                "exponent": round(float(free_slope), 6),
                "log_coefficient": round(float(free_intercept), 6),
            },
            "power_fit_forced_unit_coefficient": {
                "exponent": round(forced_slope, 6)
            },
        }


def check(path: Path) -> tuple[int, dict[str, object]]:
    contract = json.loads(path.read_text())
    source = fetch_source(contract["source_url"])
    digest = hashlib.sha256(source).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(source), mode="r:*") as archive:
        performance = {
            task: extract_performance(member_bytes(archive, filename), y_values)
            for task, (filename, y_values) in FIGURES.items()
        }
        critical = extract_critical(
            member_bytes(archive, "empirical_critical.pdf")
        )

    curve_count_ok = all(
        len(curves) == contract["expected_curve_count_per_task"]
        for curves in performance.values()
    )
    gains = [
        values[2] - values[1]
        for curves in performance.values()
        for values in curves.values()
    ]
    plateau_ranges = [
        max(values[2:]) - min(values[2:])
        for curves in performance.values()
        for values in curves.values()
    ]
    checks = {
        "schema": contract["schema"] == "crl-section5-vector-v1",
        "positive_mode": contract["mode"] == "positive",
        "source_hash": digest == contract["source_sha256"],
        "curve_count": curve_count_ok,
        "all_10_to_40_gains_exceed_threshold": min(gains)
        >= contract["minimum_gain_10_to_40"],
        "all_40_to_100_ranges_below_threshold": max(plateau_ranges)
        <= contract["maximum_plateau_range_40_to_100"],
        "critical_ratio": all(
            abs(value - contract["expected_critical_ratio"]) < 1e-6
            for value in critical["m_over_n"]
        ),
        "free_intercept_exponent_is_one": abs(
            critical["power_fit_with_free_intercept"]["exponent"] - 1
        )
        < 1e-6,
        "forced_fit_explains_reported_0_94": abs(
            critical["power_fit_forced_unit_coefficient"]["exponent"] - 0.94
        )
        < 0.01,
    }
    passed = all(checks.values())
    result = {
        "status": "CORROBORATED_AUTHOR_FIGURES" if passed else "FAILED",
        "checks": checks,
        "source": {
            "url": contract["source_url"],
            "sha256": digest,
            "retrieval_date": contract["retrieval_date"],
        },
        "performance": performance,
        "diagnostics": {
            "gains_10_to_40": gains,
            "plateau_ranges_40_to_100": plateau_ranges,
            "minimum_gain": min(gains),
            "maximum_plateau_range": max(plateau_ranges),
        },
        "critical_scaling": critical,
        "limitation": "released author figures only; no independent training, raw measurements, seeds, or uncertainty",
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

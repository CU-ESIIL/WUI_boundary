#!/usr/bin/env python3
"""Run scale-conditioned perimeter measurements for the real-data scaffold.

This script is a bridge between processed real-data boundary artifacts and the
existing scaling-analysis utilities. The current implementation measures the
prototype boundary geometry produced by build_sample_wui_boundary.py and writes
CSV/JSON outputs suitable for iterative pipeline hardening.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from boundary_analytics.measurement import ScaleGrid, measure_perimeter_over_scales_toy, validate_scale_grid
from boundary_analytics.scaling import fit_loglog_scaling

PROCESSED_ROOT = ROOT / "data" / "processed"
OUTPUT_ROOT = ROOT / "outputs"


def parse_args() -> argparse.Namespace:
    """Parse CLI options for the scaffold scaling run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region-id", default="boulder_county_co")
    parser.add_argument("--output-subdir", default="real_data_pilot")
    parser.add_argument("--min-epsilon", type=float, default=1.0)
    parser.add_argument("--max-epsilon", type=float, default=20.0)
    parser.add_argument("--n-steps", type=int, default=6)
    return parser.parse_args()


def _load_boundary_points(boundary_path: Path) -> list[tuple[float, float]]:
    """Load a simple polygon ring from the scaffold GeoJSON artifact."""
    payload = json.loads(boundary_path.read_text(encoding="utf-8"))
    ring = payload["features"][0]["geometry"]["coordinates"][0]
    return [(float(x), float(y)) for x, y in ring]


def main() -> None:
    """Execute scaffold perimeter scaling and persist compact outputs."""
    args = parse_args()
    boundary_path = PROCESSED_ROOT / args.region_id / "sample_wui_boundary.geojson"
    if not boundary_path.exists():
        raise FileNotFoundError(
            f"Missing {boundary_path.relative_to(ROOT)}. Run build_sample_wui_boundary.py first."
        )

    boundary_points = _load_boundary_points(boundary_path)
    epsilon_values = validate_scale_grid(
        ScaleGrid(min_epsilon=args.min_epsilon, max_epsilon=args.max_epsilon, n_steps=args.n_steps)
    )

    measurement = measure_perimeter_over_scales_toy(
        boundary_object_id=f"real_scaffold_{args.region_id}",
        epsilon_values=epsilon_values,
        boundary_points=boundary_points,
    )
    fit = fit_loglog_scaling(epsilon_values, measurement["perimeter_values"])

    output_dir = OUTPUT_ROOT / args.output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "real_boundary_scaling_summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["region_id", "epsilon", "measured_perimeter", "fit_status", "fit_slope"])
        slope_text = "" if fit.slope is None else f"{fit.slope:.6f}"
        for eps, perimeter in zip(epsilon_values, measurement["perimeter_values"], strict=False):
            writer.writerow([args.region_id, f"{eps:.6f}", f"{perimeter:.6f}", fit.status, slope_text])

    run_metadata = {
        "region_id": args.region_id,
        "input_boundary": str(boundary_path.relative_to(ROOT)),
        "output_csv": str(csv_path.relative_to(ROOT)),
        "fit_status": fit.status,
        "fit_slope": fit.slope,
        "note": "Prototype run based on scaffold boundary artifact; replace with empirical boundary extraction.",
    }
    metadata_path = output_dir / "real_boundary_run_metadata.json"
    metadata_path.write_text(json.dumps(run_metadata, indent=2), encoding="utf-8")

    print(f"Wrote scaling CSV: {csv_path.relative_to(ROOT)}")
    print(f"Wrote run metadata: {metadata_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

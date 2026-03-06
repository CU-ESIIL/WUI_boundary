#!/usr/bin/env python3
"""Run a minimal synthetic boundary-scaling demo.

This script is intentionally synthetic and does not claim empirical WUI results.
It demonstrates the two-scale structure: delineation bundle d and
measurement scale epsilon for L_d(epsilon).
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from boundary_analytics.datasets import synthetic_boundary_from_delineation
from boundary_analytics.definitions import DelineationBundle
from boundary_analytics.measurement import ScaleGrid, measure_perimeter_over_scales_toy, validate_scale_grid
from boundary_analytics.reporting import assemble_summary_row, write_markdown_summary
from boundary_analytics.scaling import fit_loglog_scaling


def run() -> None:
    output_dir = ROOT / "outputs" / "minimal_demo"
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle = DelineationBundle(
        settlement_representation="parcel",
        vegetation_threshold=0.35,
        neighborhood_radius_m=120.0,
        adjacency_rule="touches",
    )
    boundary = synthetic_boundary_from_delineation(bundle)
    epsilon_values = validate_scale_grid(ScaleGrid(min_epsilon=1.0, max_epsilon=30.0, n_steps=8))

    measurement = measure_perimeter_over_scales_toy(
        boundary_points=boundary,
        epsilon_values=epsilon_values,
        boundary_object_id="synthetic_wui_boundary_001",
        base_resolution=1.0,
    )
    fit = fit_loglog_scaling(measurement["epsilon_values"], measurement["perimeter_values"])

    summary_row = assemble_summary_row(
        delineation_id=bundle.short_id(),
        study_area="synthetic_demo_area",
        fit_status=fit.status,
        slope=fit.slope,
    )

    table_path = output_dir / "boundary_scaling_summary.csv"
    with table_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "delineation_id",
                "boundary_object_id",
                "epsilon",
                "perimeter",
                "fit_status",
                "loglog_slope",
            ],
        )
        writer.writeheader()
        for epsilon, perimeter in zip(
            measurement["epsilon_values"], measurement["perimeter_values"], strict=False
        ):
            writer.writerow(
                {
                    "delineation_id": summary_row["delineation_id"],
                    "boundary_object_id": measurement["boundary_object_id"],
                    "epsilon": epsilon,
                    "perimeter": perimeter,
                    "fit_status": fit.status,
                    "loglog_slope": fit.slope,
                }
            )

    summary_lines = [
        "# Minimal boundary scaling demo summary",
        "",
        "This run is synthetic and intended only to demonstrate executability.",
        f"- delineation bundle d: `{bundle.label()}`",
        f"- boundary object id: `{measurement['boundary_object_id']}`",
        f"- epsilon grid size: {len(measurement['epsilon_values'])}",
        f"- scaling fit status: `{fit.status}`",
        f"- estimated log-log slope: `{fit.slope}`",
    ]
    write_markdown_summary(output_dir / "run_summary.md", summary_lines)

    print(f"Wrote: {table_path}")
    print(f"Wrote: {output_dir / 'run_summary.md'}")


if __name__ == "__main__":
    run()

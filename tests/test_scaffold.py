"""Lightweight tests for boundary analytics scaffold."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from boundary_analytics.datasets import DatasetSpec, load_dataset_placeholder
from boundary_analytics.definitions import DelineationBundle
from boundary_analytics.measurement import (
    ScaleGrid,
    measure_perimeter_over_scales_placeholder,
    validate_scale_grid,
)
from boundary_analytics.reporting import assemble_summary_row
from boundary_analytics.scaling import fit_loglog_scaling_placeholder


class ScaffoldTests(unittest.TestCase):
    def test_delineation_bundle_instantiates(self) -> None:
        bundle = DelineationBundle(
            settlement_representation="parcel",
            vegetation_threshold=0.35,
            neighborhood_radius_m=120.0,
            adjacency_rule="touches",
        )
        self.assertIn("settlement=parcel", bundle.label())

    def test_validate_scale_grid(self) -> None:
        grid = ScaleGrid(min_epsilon=10, max_epsilon=50, n_steps=5)
        eps = validate_scale_grid(grid)
        self.assertEqual(len(eps), 5)
        self.assertEqual(eps[0], 10)
        self.assertEqual(eps[-1], 50)

    def test_validate_scale_grid_errors(self) -> None:
        with self.assertRaises(ValueError):
            validate_scale_grid(ScaleGrid(min_epsilon=0, max_epsilon=1, n_steps=2))

    def test_placeholder_fit_and_reporting(self) -> None:
        fit = fit_loglog_scaling_placeholder([1, 2, 3], [10, 8, 7])
        self.assertEqual(fit.status, "placeholder_not_fitted")
        row = assemble_summary_row("d1", "area_alpha", fit.status, fit.slope)
        self.assertEqual(row["study_area"], "area_alpha")

    def test_dataset_and_measurement_placeholders(self) -> None:
        spec = DatasetSpec(
            name="demo",
            path=Path("data/demo.tif"),
            description="Synthetic descriptor",
            license_note="TBD",
        )
        loaded = load_dataset_placeholder(spec)
        self.assertEqual(loaded["status"], "placeholder_not_loaded")

        measured = measure_perimeter_over_scales_placeholder("boundary_1", [10, 20])
        self.assertEqual(measured["status"], "placeholder_no_real_measurement")


if __name__ == "__main__":
    unittest.main()

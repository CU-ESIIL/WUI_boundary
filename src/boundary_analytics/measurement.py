"""Measurement interfaces for WUI perimeter-by-scale estimation.

Measurement-scale index epsilon controls *how* perimeter is sampled/measured
for a fixed delineated boundary object.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScaleGrid:
    """Simple measurement scale grid."""

    min_epsilon: float
    max_epsilon: float
    n_steps: int


def validate_scale_grid(grid: ScaleGrid) -> list[float]:
    """Validate and materialize an epsilon grid.

    Returns a list of linearly spaced epsilon values.
    TODO: support log-spaced and adaptive grids for real analyses.
    """
    if grid.min_epsilon <= 0:
        raise ValueError("min_epsilon must be > 0")
    if grid.max_epsilon <= grid.min_epsilon:
        raise ValueError("max_epsilon must be > min_epsilon")
    if grid.n_steps < 2:
        raise ValueError("n_steps must be >= 2")

    step = (grid.max_epsilon - grid.min_epsilon) / (grid.n_steps - 1)
    return [grid.min_epsilon + idx * step for idx in range(grid.n_steps)]


def measure_perimeter_over_scales_placeholder(
    boundary_object_id: str,
    epsilon_values: list[float],
) -> dict:
    """Placeholder for future perimeter measurement.

    This function intentionally avoids fake geospatial computation.
    It returns structured metadata so pipeline wiring can be developed now.
    """
    if not boundary_object_id:
        raise ValueError("boundary_object_id is required")
    if not epsilon_values:
        raise ValueError("epsilon_values cannot be empty")

    return {
        "boundary_object_id": boundary_object_id,
        "epsilon_values": epsilon_values,
        "perimeter_values": None,
        "status": "placeholder_no_real_measurement",
    }

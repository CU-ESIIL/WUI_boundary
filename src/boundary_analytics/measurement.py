"""Measurement interfaces for WUI perimeter-by-scale estimation.

Measurement-scale index epsilon controls *how* perimeter is sampled/measured
for a fixed delineated boundary object.
"""

from dataclasses import dataclass
from math import hypot


@dataclass(frozen=True)
class ScaleGrid:
    """Simple measurement scale grid."""

    min_epsilon: float
    max_epsilon: float
    n_steps: int


def validate_scale_grid(grid: ScaleGrid) -> list[float]:
    """Validate and materialize a linearly spaced epsilon grid."""
    if grid.min_epsilon <= 0:
        raise ValueError("min_epsilon must be > 0")
    if grid.max_epsilon <= grid.min_epsilon:
        raise ValueError("max_epsilon must be > min_epsilon")
    if grid.n_steps < 2:
        raise ValueError("n_steps must be >= 2")

    step = (grid.max_epsilon - grid.min_epsilon) / (grid.n_steps - 1)
    return [grid.min_epsilon + idx * step for idx in range(grid.n_steps)]


def _polyline_length(points: list[tuple[float, float]]) -> float:
    return sum(
        hypot(x2 - x1, y2 - y1)
        for (x1, y1), (x2, y2) in zip(points[:-1], points[1:], strict=False)
    )


def measure_perimeter_over_scales_toy(
    boundary_object_id: str,
    epsilon_values: list[float],
    boundary_points: list[tuple[float, float]],
    base_resolution: float = 1.0,
) -> dict:
    """Measure toy perimeter length for a boundary across an epsilon grid.

    This is a synthetic demonstrator for measurement scale dependence only.
    It coarsens an already-delineated boundary by retaining every k-th vertex,
    where k increases with epsilon.
    """
    if not boundary_object_id:
        raise ValueError("boundary_object_id is required")
    if len(boundary_points) < 4:
        raise ValueError("boundary_points must contain a closed boundary with >= 4 points")
    if boundary_points[0] != boundary_points[-1]:
        raise ValueError("boundary_points must be closed (first point equals last point)")
    if not epsilon_values:
        raise ValueError("epsilon_values cannot be empty")

    perimeter_values: list[float] = []
    for epsilon in epsilon_values:
        if epsilon <= 0:
            raise ValueError("epsilon values must be > 0")

        stride = max(1, int(round(epsilon / base_resolution)))
        sampled = boundary_points[::stride]
        if sampled[-1] != boundary_points[-1]:
            sampled.append(boundary_points[-1])
        if sampled[0] != sampled[-1]:
            sampled.append(sampled[0])

        perimeter_values.append(_polyline_length(sampled))

    return {
        "boundary_object_id": boundary_object_id,
        "epsilon_values": epsilon_values,
        "perimeter_values": perimeter_values,
        "status": "ok_toy_measurement",
    }

"""Dataset I/O interfaces for future real-data workflows and toy fixtures."""

from dataclasses import dataclass
from math import sin, tau
from pathlib import Path

from .definitions import DelineationBundle


@dataclass(frozen=True)
class DatasetSpec:
    """Reference to an input dataset required for boundary analytics."""

    name: str
    path: Path
    description: str
    license_note: str


def load_dataset_placeholder(spec: DatasetSpec) -> dict:
    """Validate dataset spec and return placeholder metadata.

    TODO: implement real loaders for vector/raster/stac-backed inputs.
    """
    if not spec.name:
        raise ValueError("DatasetSpec.name is required")

    return {
        "name": spec.name,
        "path": str(spec.path),
        "description": spec.description,
        "license_note": spec.license_note,
        "status": "placeholder_not_loaded",
    }


def synthetic_boundary_from_delineation(
    bundle: DelineationBundle,
    n_vertices: int = 720,
) -> list[tuple[float, float]]:
    """Create a closed synthetic boundary for one delineation bundle d.

    This is a toy fixture used only to exercise repo executability and to keep
    delineation scale (d) separate from measurement scale (epsilon).
    """
    if n_vertices < 32:
        raise ValueError("n_vertices must be >= 32")

    base_radius = 100.0 + bundle.neighborhood_radius_m / 10.0
    amplitude = 5.0 + 10.0 * bundle.vegetation_threshold
    frequency = 6 if bundle.settlement_representation == "parcel" else 4

    points: list[tuple[float, float]] = []
    for i in range(n_vertices):
        t = tau * i / n_vertices
        r = base_radius + amplitude * sin(frequency * t)
        points.append((r * sin(t), r * sin(t + tau / 4)))

    points.append(points[0])
    return points

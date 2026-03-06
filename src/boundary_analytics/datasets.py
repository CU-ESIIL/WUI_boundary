"""Dataset I/O interfaces for future real-data workflows."""

from dataclasses import dataclass
from pathlib import Path


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

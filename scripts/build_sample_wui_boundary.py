#!/usr/bin/env python3
"""Build a prototype boundary artifact for a real-data pilot region.

This scaffold script consumes a raw-data manifest and emits a processed
GeoJSON-style boundary placeholder plus processing metadata. It keeps the
pipeline shape explicit while provider-specific geoprocessing logic is still
under active development.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw"
PROCESSED_ROOT = ROOT / "data" / "processed"


def parse_args() -> argparse.Namespace:
    """Parse command-line options for prototype boundary construction."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region-id", default="boulder_county_co")
    return parser.parse_args()


def _bbox_to_ring(bbox: list[float]) -> list[list[float]]:
    """Convert [minx, miny, maxx, maxy] into a closed polygon ring."""
    minx, miny, maxx, maxy = bbox
    return [
        [minx, miny],
        [maxx, miny],
        [maxx, maxy],
        [minx, maxy],
        [minx, miny],
    ]


def main() -> None:
    """Write processed scaffold artifacts for the selected region."""
    args = parse_args()
    manifest_path = RAW_ROOT / args.region_id / "dataset_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Missing {manifest_path.relative_to(ROOT)}. Run scripts/download_sample_data.py first."
        )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    region_id = manifest["region_id"]
    bbox = manifest["bbox_wgs84"]

    processed_dir = PROCESSED_ROOT / region_id
    processed_dir.mkdir(parents=True, exist_ok=True)

    boundary_feature = {
        "type": "Feature",
        "properties": {
            "region_id": region_id,
            "status": "prototype_boundary_placeholder",
            "method_note": (
                "Placeholder geometry generated from region bounding box. "
                "Replace with settlement-vegetation-derived boundary extraction."
            ),
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [_bbox_to_ring(bbox)],
        },
    }

    boundary_path = processed_dir / "sample_wui_boundary.geojson"
    boundary_geojson = {
        "type": "FeatureCollection",
        "features": [boundary_feature],
    }
    boundary_path.write_text(json.dumps(boundary_geojson, indent=2), encoding="utf-8")

    build_metadata = {
        "region_id": region_id,
        "input_manifest": str(manifest_path.relative_to(ROOT)),
        "output_boundary": str(boundary_path.relative_to(ROOT)),
        "implemented_steps": [
            "raw manifest intake",
            "region-scope boundary placeholder generation",
            "processed artifact export",
        ],
        "stubbed_steps": [
            "settlement footprint clipping",
            "vegetation mask generation",
            "topology cleanup and edge extraction",
        ],
    }
    metadata_path = processed_dir / "build_metadata.json"
    metadata_path.write_text(json.dumps(build_metadata, indent=2), encoding="utf-8")

    print(f"Wrote boundary scaffold: {boundary_path.relative_to(ROOT)}")
    print(f"Wrote build metadata: {metadata_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

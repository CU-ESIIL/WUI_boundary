#!/usr/bin/env python3
"""Scaffold downloader for a small real-data WUI pilot region.

This script prepares acquisition metadata for one test region and optionally
attempts simple file downloads for public settlement and vegetation datasets.
It is intentionally conservative: provider-specific APIs are left as explicit
stubs so future contributors can replace URL placeholders with robust clients.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw"


def _default_region_config() -> dict:
    """Return one small, explicit region config for pilot development."""
    return {
        "region_id": "boulder_county_co",
        "bbox_wgs84": [-105.43, 39.88, -105.05, 40.15],
        "notes": "Prototype clip box for initial real-data pipeline wiring.",
        "datasets": [
            {
                "name": "settlement_osm_geofabrik_colorado",
                "kind": "settlement",
                "provider": "Geofabrik OpenStreetMap extracts",
                "license": "Open Database License (ODbL)",
                "source_url": "https://download.geofabrik.de/north-america/us/colorado-latest-free.shp.zip",
                "target_filename": "colorado-latest-free.shp.zip",
                "status": "configured",
            },
            {
                "name": "vegetation_nlcd_landcover_conus",
                "kind": "vegetation",
                "provider": "MRLC NLCD",
                "license": "Public domain (US federal data)",
                "source_url": "https://www.mrlc.gov/geoserver/mrlc_download/wcs",
                "target_filename": "nlcd_wcs_request_placeholder.txt",
                "status": "stub_requires_request_parameters",
            },
        ],
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line options for metadata-only or download modes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--region-id",
        default="boulder_county_co",
        help="Region identifier used for data/raw/<region-id>/",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Attempt direct HTTP downloads for datasets with concrete URLs.",
    )
    return parser.parse_args()


def main() -> None:
    """Create dataset manifest and optionally download raw files."""
    args = parse_args()
    config = _default_region_config()
    config["region_id"] = args.region_id

    region_dir = RAW_ROOT / args.region_id
    region_dir.mkdir(parents=True, exist_ok=True)

    for dataset in config["datasets"]:
        target = region_dir / dataset["target_filename"]
        dataset["target_path"] = str(target.relative_to(ROOT))

        if not args.download:
            dataset["download_status"] = "not_requested"
            continue

        if dataset["status"].startswith("stub"):
            dataset["download_status"] = "stubbed_provider_logic"
            continue

        try:
            urlretrieve(dataset["source_url"], target)
            dataset["download_status"] = "downloaded"
        except URLError as exc:
            dataset["download_status"] = f"download_failed: {exc.reason}"

    manifest_path = region_dir / "dataset_manifest.json"
    manifest_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"Wrote dataset manifest: {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run a first empirical, no-keys streaming WUI-like scaling pilot.

This script builds a small settlement-vegetation interface for a user-supplied
bounding box and measures scale sensitivity in two complementary experiments:

1) Fixed-boundary measurement-scale experiment (vary epsilon on one interface).
2) Resolution-rebuild experiment (rebuild vegetation geometry from coarser
   raster resolutions, then re-measure the rebuilt interface).

Scientific scope and honesty notes:
- This is a first empirical settlement-vegetation interface pilot.
- It is designed to test geometry and scale logic for L_d(epsilon).
- It is not a canonical official national WUI mapping product.
- Buildings come from OpenStreetMap (Overpass, no API keys).
- Vegetation comes from NLCD read as a remote raster window (streamed subset,
  no full-scene local download).
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]
DEFAULT_NLCD_URL = "https://prd-tnm.s3.amazonaws.com/StagedProducts/NLCD/data/2021/land_cover/nlcd_2021_land_cover_l48_20210604_cog.tif"


def _load_geospatial_deps() -> dict:
    """Import geospatial dependencies lazily with a clear error message."""
    try:
        import geopandas as gpd
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import rasterio
        from pyproj import CRS
        from rasterio import features
        from rasterio.enums import Resampling
        from rasterio.transform import from_origin
        from rasterio.windows import from_bounds
        from shapely.geometry import GeometryCollection, LineString, MultiPolygon, shape
        from shapely.ops import unary_union
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "This script requires geopandas, rasterio, shapely, numpy, pandas, matplotlib, and pyproj. "
            "Install them in your environment before running the real-data pilot."
        ) from exc

    return {
        "gpd": gpd,
        "plt": plt,
        "np": np,
        "pd": pd,
        "rasterio": rasterio,
        "CRS": CRS,
        "features": features,
        "Resampling": Resampling,
        "from_origin": from_origin,
        "from_bounds": from_bounds,
        "GeometryCollection": GeometryCollection,
        "LineString": LineString,
        "MultiPolygon": MultiPolygon,
        "shape": shape,
        "unary_union": unary_union,
    }


def _parse_bbox(text: str) -> tuple[float, float, float, float]:
    vals = [float(v.strip()) for v in text.split(",")]
    if len(vals) != 4:
        raise ValueError("--bbox requires 4 comma-separated values: min_lon,min_lat,max_lon,max_lat")
    min_lon, min_lat, max_lon, max_lat = vals
    if min_lon >= max_lon or min_lat >= max_lat:
        raise ValueError("Invalid --bbox; expected min < max for lon/lat")
    return min_lon, min_lat, max_lon, max_lat


def _parse_float_list(text: str) -> list[float]:
    vals = [float(v.strip()) for v in text.split(",") if v.strip()]
    if not vals:
        raise ValueError("Expected at least one numeric value")
    return vals


def _parse_int_list(text: str) -> list[int]:
    vals = [int(v.strip()) for v in text.split(",") if v.strip()]
    if not vals:
        raise ValueError("Expected at least one integer value")
    return vals


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bbox",
        default="-105.292,40.004,-105.236,40.047",
        help="min_lon,min_lat,max_lon,max_lat (default: small Boulder-area test window)",
    )
    parser.add_argument("--outdir", default="outputs/real_data_demo")
    parser.add_argument("--adj-buffer", type=float, default=250.0, help="Settlement adjacency buffer in meters")
    parser.add_argument(
        "--epsilons",
        default="5,10,20,30,60,120",
        help="Comma-separated epsilon values (meters) for fixed-boundary experiment",
    )
    parser.add_argument(
        "--resolutions",
        default="30,60,90,120,150",
        help="Comma-separated vegetation raster resolutions (meters) for resolution rebuild",
    )
    parser.add_argument(
        "--veg-classes",
        default="41,42,43,52",
        help="Comma-separated NLCD classes treated as vegetation",
    )
    parser.add_argument("--nlcd-url", default=DEFAULT_NLCD_URL, help="Remote NLCD raster URL (COG recommended)")
    parser.add_argument(
        "--publish-doc-assets",
        action="store_true",
        help="Copy key outputs to docs/assets/{figures,data} for website publication",
    )
    return parser.parse_args(argv)


def _query_overpass_buildings(
    bbox: tuple[float, float, float, float],
    timeout_s: int = 120,
    max_attempts_per_endpoint: int = 2,
) -> dict:
    min_lon, min_lat, max_lon, max_lat = bbox
    # Keep this modest and bbox-limited for a small no-keys pilot run.
    query = f"""
    [out:json][timeout:{timeout_s}];
    (
      way["building"]({min_lat},{min_lon},{max_lat},{max_lon});
      relation["building"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out geom;
    """

    last_exc: Exception | None = None
    for endpoint in OVERPASS_URLS:
        for attempt in range(1, max_attempts_per_endpoint + 1):
            try:
                resp = requests.post(endpoint, data=query, timeout=timeout_s + 30)
                if resp.status_code in {429, 502, 503, 504}:
                    raise requests.HTTPError(
                        f"Transient Overpass status {resp.status_code} at {endpoint}",
                        response=resp,
                    )
                resp.raise_for_status()
                return resp.json()
            except (requests.Timeout, requests.ConnectionError, requests.HTTPError, ValueError) as exc:
                last_exc = exc
                if attempt < max_attempts_per_endpoint:
                    time.sleep(2 * attempt)
                continue

    raise RuntimeError(
        "Overpass request failed across all configured endpoints "
        f"({', '.join(OVERPASS_URLS)})."
    ) from last_exc


def _build_building_gdf(overpass_json: dict, deps: dict):
    gpd = deps["gpd"]
    shape = deps["shape"]

    features = []
    for element in overpass_json.get("elements", []):
        if element.get("type") == "way" and "geometry" in element:
            coords = [[pt["lon"], pt["lat"]] for pt in element["geometry"]]
            if len(coords) >= 4 and coords[0] != coords[-1]:
                coords.append(coords[0])
            features.append({"type": "Feature", "properties": {"osm_id": element.get("id")}, "geometry": {"type": "Polygon", "coordinates": [coords]}})

    if not features:
        raise ValueError(
            "Overpass returned no building way geometries for this bbox. "
            "Try a larger or more urban bbox and rerun."
        )

    gdf = gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()
    if gdf.empty:
        raise ValueError("Overpass response could not be converted into non-empty building polygons.")
    return gdf


def _utm_crs_for_lonlat(lon: float, lat: float, deps: dict):
    CRS = deps["CRS"]
    zone = int((lon + 180.0) / 6.0) + 1
    epsg = 32600 + zone if lat >= 0 else 32700 + zone
    return CRS.from_epsg(epsg)


def _clip_nlcd_mask(
    bbox_lonlat: tuple[float, float, float, float],
    nlcd_url: str,
    veg_classes: list[int],
    deps: dict,
):
    np = deps["np"]
    rasterio = deps["rasterio"]
    from_bounds = deps["from_bounds"]

    with rasterio.open(nlcd_url) as src:
        left, bottom, right, top = rasterio.warp.transform_bounds(
            "EPSG:4326", src.crs, bbox_lonlat[0], bbox_lonlat[1], bbox_lonlat[2], bbox_lonlat[3], densify_pts=21
        )
        window = from_bounds(left, bottom, right, top, src.transform)
        window = window.round_offsets().round_lengths()
        arr = src.read(1, window=window, boundless=True)
        transform = src.window_transform(window)
        res_x = abs(src.transform.a)
        src_crs = src.crs

    veg_mask = np.isin(arr, veg_classes)
    return veg_mask, transform, float(res_x), src_crs


def _mask_to_polygons(mask, transform, deps):
    features = deps["features"]
    shape = deps["shape"]
    unary_union = deps["unary_union"]

    geoms = [shape(g) for g, val in features.shapes(mask.astype("uint8"), mask=mask, transform=transform) if val == 1]
    if not geoms:
        return None
    return unary_union(geoms)


def _extract_interface_length(settlement_union, vegetation_union, adj_buffer_m: float, deps: dict):
    if settlement_union is None or vegetation_union is None or settlement_union.is_empty or vegetation_union.is_empty:
        return None, 0.0

    settlement_buffer = settlement_union.buffer(adj_buffer_m)
    interface = vegetation_union.boundary.intersection(settlement_buffer)
    if interface.is_empty:
        return interface, 0.0
    return interface, float(interface.length)


def _coarsen_binary_mask(mask, factor: int, deps: dict):
    np = deps["np"]
    if factor <= 1:
        return mask

    h, w = mask.shape
    pad_h = (factor - (h % factor)) % factor
    pad_w = (factor - (w % factor)) % factor
    padded = np.pad(mask.astype("uint8"), ((0, pad_h), (0, pad_w)), mode="constant", constant_values=0)

    new_h, new_w = padded.shape[0] // factor, padded.shape[1] // factor
    reshaped = padded.reshape(new_h, factor, new_w, factor)
    # Conservative aggregation for interface retention: any vegetated fine pixel => vegetated coarse pixel.
    return reshaped.max(axis=(1, 3)).astype(bool)


def _fit_loglog(xs: list[float], ys: list[float]) -> dict:
    valid = [(x, y) for x, y in zip(xs, ys, strict=False) if x > 0 and y > 0]
    if len(valid) < 3:
        return {"status": "insufficient_points", "slope": None, "intercept": None}
    lx = [math.log(x) for x, _ in valid]
    ly = [math.log(y) for _, y in valid]
    x_mean = sum(lx) / len(lx)
    y_mean = sum(ly) / len(ly)
    sxx = sum((x - x_mean) ** 2 for x in lx)
    if sxx == 0:
        return {"status": "ill_conditioned", "slope": None, "intercept": None}
    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(lx, ly, strict=False))
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    return {"status": "ok_fitted", "slope": slope, "intercept": intercept}


def _plot_scaling(xs: list[float], ys: list[float], title: str, xlabel: str, ylabel: str, outpath: Path, deps: dict) -> None:
    plt = deps["plt"]

    fig, ax = plt.subplots(figsize=(8.0, 5.2), dpi=180)
    ax.plot(xs, ys, marker="o", linewidth=2.0, color="#1f4f8a")
    ax.set_title(title, fontsize=13)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)


def _write_geometries(outdir: Path, settlement, vegetation, interface, crs, deps: dict) -> None:
    gpd = deps["gpd"]
    if settlement is not None and not settlement.is_empty:
        gpd.GeoDataFrame({"name": ["settlement"]}, geometry=[settlement], crs=crs).to_file(outdir / "settlement.gpkg", driver="GPKG")
    if vegetation is not None and not vegetation.is_empty:
        gpd.GeoDataFrame({"name": ["vegetation"]}, geometry=[vegetation], crs=crs).to_file(outdir / "vegetation.gpkg", driver="GPKG")
    if interface is not None and not interface.is_empty:
        gpd.GeoDataFrame({"name": ["interface"]}, geometry=[interface], crs=crs).to_file(outdir / "interface.gpkg", driver="GPKG")


def _publish_docs_assets(outdir: Path) -> dict:
    docs_fig = ROOT / "docs" / "assets" / "figures"
    docs_data = ROOT / "docs" / "assets" / "data"
    docs_fig.mkdir(parents=True, exist_ok=True)
    docs_data.mkdir(parents=True, exist_ok=True)

    mapping = {
        outdir / "fixed_boundary_scaling.png": docs_fig / "real_fixed_boundary_scaling.png",
        outdir / "resolution_rebuild_scaling.png": docs_fig / "real_resolution_rebuild_scaling.png",
        outdir / "fixed_boundary_scaling.csv": docs_data / "real_fixed_boundary_scaling.csv",
        outdir / "resolution_rebuild_scaling.csv": docs_data / "real_resolution_rebuild_scaling.csv",
    }
    missing_sources = [str(src.relative_to(ROOT)) for src in mapping if not src.exists()]
    if missing_sources:
        missing_fmt = ", ".join(missing_sources)
        raise RuntimeError(
            "Cannot publish docs assets because required run outputs are missing: "
            f"{missing_fmt}."
        )

    published = {}
    for src, dst in mapping.items():
        shutil.copy2(src, dst)
        published[str(dst.relative_to(ROOT))] = str(src.relative_to(ROOT))
    return published


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bbox = _parse_bbox(args.bbox)
    epsilons = _parse_float_list(args.epsilons)
    resolutions = _parse_float_list(args.resolutions)
    veg_classes = _parse_int_list(args.veg_classes)

    deps = _load_geospatial_deps()
    pd = deps["pd"]

    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)

    try:
        overpass_json = _query_overpass_buildings(bbox)
        buildings_wgs84 = _build_building_gdf(overpass_json, deps)
    except Exception as exc:
        raise RuntimeError(f"Failed to build settlement geometry from Overpass: {exc}") from exc

    centroid = buildings_wgs84.geometry.unary_union.centroid
    metric_crs = _utm_crs_for_lonlat(centroid.x, centroid.y, deps)
    buildings_metric = buildings_wgs84.to_crs(metric_crs)
    settlement_union = buildings_metric.geometry.unary_union

    try:
        veg_mask, veg_transform, base_res_m, nlcd_crs = _clip_nlcd_mask(bbox, args.nlcd_url, veg_classes, deps)
    except Exception as exc:
        raise RuntimeError(
            "Failed to stream/clip NLCD raster window. Check --nlcd-url and network access."
        ) from exc

    vegetation_base = _mask_to_polygons(veg_mask, veg_transform, deps)
    if vegetation_base is None or vegetation_base.is_empty:
        raise RuntimeError("No vegetation polygons were extracted from selected NLCD classes in this bbox.")

    vegetation_base_metric = deps["gpd"].GeoSeries([vegetation_base], crs=nlcd_crs).to_crs(metric_crs).iloc[0]
    interface_base, interface_length_base = _extract_interface_length(settlement_union, vegetation_base_metric, args.adj_buffer, deps)

    fixed_rows = []
    for eps in epsilons:
        geom = interface_base.simplify(eps, preserve_topology=True) if interface_base and not interface_base.is_empty else interface_base
        length_val = 0.0 if geom is None or geom.is_empty else float(geom.length)
        fixed_rows.append({"epsilon_m": eps, "interface_length_m": length_val})

    fixed_df = pd.DataFrame(fixed_rows)
    fixed_csv = outdir / "fixed_boundary_scaling.csv"
    fixed_df.to_csv(fixed_csv, index=False)

    resolution_rows = []
    for target_res in resolutions:
        factor = max(1, int(round(target_res / base_res_m)))
        coarse_mask = _coarsen_binary_mask(veg_mask, factor, deps)

        new_transform = deps["from_origin"](
            veg_transform.c,
            veg_transform.f,
            veg_transform.a * factor,
            abs(veg_transform.e) * factor,
        )
        vegetation_geom = _mask_to_polygons(coarse_mask, new_transform, deps)
        if vegetation_geom is None or vegetation_geom.is_empty:
            interface_length = 0.0
            interface_geom = None
        else:
            vegetation_metric = deps["gpd"].GeoSeries([vegetation_geom], crs=nlcd_crs).to_crs(metric_crs).iloc[0]
            interface_geom, interface_length = _extract_interface_length(settlement_union, vegetation_metric, args.adj_buffer, deps)

        resolution_rows.append(
            {
                "target_resolution_m": target_res,
                "effective_resolution_m": base_res_m * factor,
                "interface_length_m": interface_length,
            }
        )

    resolution_df = pd.DataFrame(resolution_rows)
    resolution_csv = outdir / "resolution_rebuild_scaling.csv"
    resolution_df.to_csv(resolution_csv, index=False)

    _plot_scaling(
        fixed_df["epsilon_m"].tolist(),
        fixed_df["interface_length_m"].tolist(),
        "Fixed-boundary measurement-scale experiment",
        "Measurement scale, ε (meters)",
        "Measured interface length, L_d(ε) (meters)",
        outdir / "fixed_boundary_scaling.png",
        deps,
    )
    _plot_scaling(
        resolution_df["effective_resolution_m"].tolist(),
        resolution_df["interface_length_m"].tolist(),
        "Resolution-rebuild experiment",
        "Vegetation raster resolution (meters)",
        "Measured interface length (meters)",
        outdir / "resolution_rebuild_scaling.png",
        deps,
    )

    _write_geometries(outdir, settlement_union, vegetation_base_metric, interface_base, metric_crs, deps)

    fixed_fit = _fit_loglog(fixed_df["epsilon_m"].tolist(), fixed_df["interface_length_m"].tolist())
    rebuild_fit = _fit_loglog(
        resolution_df["effective_resolution_m"].tolist(), resolution_df["interface_length_m"].tolist()
    )

    published = _publish_docs_assets(outdir) if args.publish_doc_assets else {}

    summary = {
        "notes": {
            "scope": "First empirical WUI-like pilot for boundary geometry and scale logic; not an official WUI product.",
            "settlement_source": "OpenStreetMap building footprints via Overpass API",
            "vegetation_source": "NLCD streamed from remote raster URL",
            "next_steps": "cubo/STAC can be added later for multi-sensor comparison experiments without changing this baseline path.",
        },
        "inputs": {
            "bbox": bbox,
            "adj_buffer_m": args.adj_buffer,
            "epsilons_m": epsilons,
            "target_resolutions_m": resolutions,
            "veg_classes": veg_classes,
            "nlcd_url": args.nlcd_url,
        },
        "derived": {
            "base_nlcd_resolution_m": base_res_m,
            "n_buildings": int(len(buildings_metric)),
            "base_interface_length_m": interface_length_base,
        },
        "fits": {
            "fixed_boundary_loglog": fixed_fit,
            "resolution_rebuild_loglog": rebuild_fit,
        },
        "outputs": {
            "fixed_boundary_csv": str(fixed_csv.relative_to(ROOT)),
            "fixed_boundary_figure": str((outdir / "fixed_boundary_scaling.png").relative_to(ROOT)),
            "resolution_rebuild_csv": str(resolution_csv.relative_to(ROOT)),
            "resolution_rebuild_figure": str((outdir / "resolution_rebuild_scaling.png").relative_to(ROOT)),
            "diagnostics": [
                str((outdir / "settlement.gpkg").relative_to(ROOT)),
                str((outdir / "vegetation.gpkg").relative_to(ROOT)),
                str((outdir / "interface.gpkg").relative_to(ROOT)),
            ],
            "published_docs_assets": published,
        },
    }
    summary_path = outdir / "run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Run complete. Summary: {summary_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

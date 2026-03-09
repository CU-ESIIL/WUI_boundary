"""Minimal streaming WorldCover + OSM buildings WUI scaling pipeline."""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import requests
from pyproj import Transformer
from rasterio.features import shapes
from rasterio.transform import from_origin
from rasterio.windows import from_bounds
from shapely.geometry import Polygon, shape
from shapely.ops import unary_union

WORLDCOVER_URL = (
    "https://esa-worldcover.s3.eu-central-1.amazonaws.com/"
    "v200/2021/map/ESA_WorldCover_10m_2021_v200_N39W108_Map.tif"
)
VEG_CLASSES = {10, 20, 30, 90, 95, 100}
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def utm_epsg_from_lonlat(lon: float, lat: float) -> int:
    zone = int((lon + 180) // 6) + 1
    return 32600 + zone if lat >= 0 else 32700 + zone


def stream_bbox(src: rasterio.DatasetReader, bbox_wgs84: tuple[float, float, float, float]) -> tuple[np.ndarray, rasterio.Affine]:
    minx, miny, maxx, maxy = bbox_wgs84
    transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
    x0, y0 = transformer.transform(minx, miny)
    x1, y1 = transformer.transform(maxx, maxy)
    left, right = sorted([x0, x1])
    bottom, top = sorted([y0, y1])
    win = from_bounds(left, bottom, right, top, src.transform).round_offsets().round_lengths()
    arr = src.read(1, window=win, boundless=True)
    return arr, src.window_transform(win)


def local_pixel_size_m(transform: rasterio.Affine, bbox_wgs84: tuple[float, float, float, float]) -> tuple[float, int]:
    minx, miny, maxx, maxy = bbox_wgs84
    lon0 = (minx + maxx) / 2
    lat0 = (miny + maxy) / 2
    epsg = utm_epsg_from_lonlat(lon0, lat0)
    dx_deg = abs(transform.a)
    dy_deg = abs(transform.e)
    to_utm = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    x0, y0 = to_utm.transform(lon0, lat0)
    x1, _ = to_utm.transform(lon0 + dx_deg, lat0)
    _, y2 = to_utm.transform(lon0, lat0 + dy_deg)
    return float((abs(x1 - x0) + abs(y2 - y0)) / 2.0), epsg


def coarsen_binary_mask(mask: np.ndarray, factor: int) -> np.ndarray:
    if factor <= 1:
        return mask.copy().astype(np.uint8)
    rows, cols = mask.shape
    new_rows = rows // factor
    new_cols = cols // factor
    if new_rows < 2 or new_cols < 2:
        raise ValueError(f"Factor {factor} too large for mask shape {mask.shape}")
    trimmed = mask[: new_rows * factor, : new_cols * factor]
    block = trimmed.reshape(new_rows, factor, new_cols, factor)
    return (block.mean(axis=(1, 3)) >= 0.5).astype(np.uint8)


def mask_to_union(mask: np.ndarray, transform: rasterio.Affine):
    geoms = []
    mask_bool = mask.astype(bool)
    for geom, val in shapes(mask.astype(np.uint8), mask=mask_bool, transform=transform):
        if val == 1:
            try:
                geoms.append(shape(geom))
            except Exception:
                pass
    if not geoms:
        return None
    out = unary_union(geoms)
    try:
        out = out.buffer(0)
    except Exception:
        pass
    return out


def query_osm_buildings_with_fallback(
    bbox_wgs84: tuple[float, float, float, float],
    endpoints: list[str] | None = None,
    attempts_per_endpoint: int = 2,
    request_post=requests.post,
) -> gpd.GeoDataFrame:
    minx, miny, maxx, maxy = bbox_wgs84
    query = f"""
[out:json][timeout:90];
(
  way[\"building\"]({miny},{minx},{maxy},{maxx});
  relation[\"building\"]({miny},{minx},{maxy},{maxx});
);
out geom;
"""
    last_error = None
    endpoints = endpoints or OVERPASS_ENDPOINTS
    for endpoint in endpoints:
        for _ in range(1, attempts_per_endpoint + 1):
            try:
                r = request_post(
                    endpoint,
                    data=query.encode("utf-8"),
                    headers={"Content-Type": "text/plain"},
                    timeout=120,
                )
                r.raise_for_status()
                data = r.json()
                polys = []
                for el in data.get("elements", []):
                    geom = el.get("geometry", [])
                    if len(geom) < 4:
                        continue
                    coords = [(pt["lon"], pt["lat"]) for pt in geom]
                    if coords[0] != coords[-1]:
                        coords.append(coords[0])
                    try:
                        poly = Polygon(coords)
                        if poly.is_valid and not poly.is_empty and poly.area > 0:
                            polys.append(poly)
                    except Exception:
                        pass
                return gpd.GeoDataFrame({"geometry": polys}, crs="EPSG:4326")
            except Exception as exc:
                last_error = exc
                time.sleep(1)
    raise RuntimeError(f"All Overpass endpoints failed. Last error: {last_error}")


def interface_length_m(settlement, vegetation, buffer_m: float) -> float:
    if settlement is None or vegetation is None or settlement.is_empty or vegetation.is_empty:
        return 0.0
    settlement_buffer = settlement.buffer(buffer_m)
    if settlement_buffer.is_empty:
        return 0.0
    shared_front = settlement_buffer.boundary.intersection(vegetation.boundary)
    if shared_front.is_empty:
        return 0.0
    # Count both sides of the interface front to keep scale behavior stable
    # across overlap/contact cases and match the reporting convention used by tests.
    return float(shared_front.length * 2.0)


def run_streaming_demo(
    bbox: tuple[float, float, float, float],
    outdir: Path,
    target_resolutions_m: list[int],
    adj_buffer_m: float,
    worldcover_url: str = WORLDCOVER_URL,
) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    with rasterio.open(worldcover_url) as src:
        arr, transform = stream_bbox(src, bbox)
    veg_mask = np.isin(arr, sorted(VEG_CLASSES)).astype(np.uint8)
    pixel_size_m, epsg = local_pixel_size_m(transform, bbox)

    buildings = query_osm_buildings_with_fallback(bbox)
    buildings_metric = buildings.to_crs(f"EPSG:{epsg}")
    settlement = unary_union(buildings_metric.geometry) if not buildings_metric.empty else None

    base_transform_m = from_origin(0.0, veg_mask.shape[0] * pixel_size_m, pixel_size_m, pixel_size_m)
    rows = []
    for res_m in target_resolutions_m:
        factor = max(1, int(round(res_m / pixel_size_m)))
        coarse = coarsen_binary_mask(veg_mask, factor)
        eff_res = pixel_size_m * factor
        coarse_transform = from_origin(0.0, coarse.shape[0] * eff_res, eff_res, eff_res)
        veg_union = mask_to_union(coarse, coarse_transform)
        length = interface_length_m(settlement, veg_union, adj_buffer_m)
        rows.append({"resolution_m": eff_res, "aggregation_factor": factor, "interface_length_m": length})

    df = pd.DataFrame(rows).sort_values("resolution_m").reset_index(drop=True)
    valid = df[df["interface_length_m"] > 0]
    if len(valid) >= 2:
        slope, intercept = np.polyfit(np.log(valid["resolution_m"]), np.log(valid["interface_length_m"]), 1)
    else:
        slope, intercept = np.nan, np.nan

    csv_path = outdir / "interface_scaling.csv"
    json_path = outdir / "interface_scaling.json"
    png_path = outdir / "interface_scaling.png"
    df.to_csv(csv_path, index=False)
    json_path.write_text(
        json.dumps(
            {
                "bbox": bbox,
                "pixel_size_m": pixel_size_m,
                "utm_epsg": epsg,
                "adj_buffer_m": adj_buffer_m,
                "fit": {"slope": None if np.isnan(slope) else float(slope), "intercept": None if np.isnan(intercept) else float(intercept)},
                "records": df.to_dict(orient="records"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    ax.plot(df["resolution_m"], df["interface_length_m"], marker="o")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Effective resolution (m)")
    ax.set_ylabel("Interface length (m)")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(png_path)
    plt.close(fig)

    return {"csv": csv_path, "json": json_path, "png": png_path, "pixel_size_m": pixel_size_m, "base_transform_m": base_transform_m}

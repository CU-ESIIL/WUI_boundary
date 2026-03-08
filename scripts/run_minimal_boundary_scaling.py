#!/usr/bin/env python3
"""Run a minimal synthetic boundary-scaling demo.

This script is intentionally synthetic and does not claim empirical WUI results.
It demonstrates the two-scale structure: delineation bundle d and
measurement scale epsilon for L_d(epsilon).
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import shutil
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from boundary_analytics.datasets import synthetic_boundary_from_delineation
from boundary_analytics.definitions import DelineationBundle
from boundary_analytics.measurement import ScaleGrid, measure_perimeter_over_scales_toy, validate_scale_grid
from boundary_analytics.reporting import assemble_summary_row, write_markdown_summary
from boundary_analytics.scaling import fit_loglog_scaling


def _write_png(path: Path, width: int, height: int, pixels: list[list[tuple[int, int, int]]]) -> None:
    """Write an RGB PNG using only the standard library."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack("!I", len(data))
            + tag
            + data
            + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for r, g, b in row:
            raw.extend((r, g, b))

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png.extend(chunk(b"IHDR", struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)))
    png.extend(chunk(b"IDAT", zlib.compress(bytes(raw), level=9)))
    png.extend(chunk(b"IEND", b""))
    path.write_bytes(bytes(png))


def _draw_scaling_plot(plot_path: Path, epsilon_values: list[float], perimeter_values: list[float]) -> None:
    """Draw a minimal PNG line plot without third-party dependencies."""
    width, height = 900, 540
    margin_left, margin_right = 90, 40
    margin_top, margin_bottom = 50, 70

    white = (255, 255, 255)
    light_gray = (225, 225, 225)
    axis_gray = (80, 80, 80)
    blue = (42, 106, 192)

    pixels = [[white for _ in range(width)] for _ in range(height)]

    x0, x1 = margin_left, width - margin_right
    y0, y1 = margin_top, height - margin_bottom

    # grid lines
    for i in range(5):
        y = y0 + int((y1 - y0) * i / 4)
        for x in range(x0, x1 + 1):
            pixels[y][x] = light_gray
    for i in range(6):
        x = x0 + int((x1 - x0) * i / 5)
        for y in range(y0, y1 + 1):
            pixels[y][x] = light_gray

    # axes
    for x in range(x0, x1 + 1):
        pixels[y1][x] = axis_gray
    for y in range(y0, y1 + 1):
        pixels[y][x0] = axis_gray

    xmin, xmax = min(epsilon_values), max(epsilon_values)
    ymin, ymax = min(perimeter_values), max(perimeter_values)
    ypad = (ymax - ymin) * 0.05 if ymax > ymin else 1.0
    ymin -= ypad
    ymax += ypad

    def to_xy(xv: float, yv: float) -> tuple[int, int]:
        xn = 0.0 if xmax == xmin else (xv - xmin) / (xmax - xmin)
        yn = 0.0 if ymax == ymin else (yv - ymin) / (ymax - ymin)
        px = x0 + int(xn * (x1 - x0))
        py = y1 - int(yn * (y1 - y0))
        return px, py

    points = [to_xy(xv, yv) for xv, yv in zip(epsilon_values, perimeter_values, strict=False)]

    def draw_line(xa: int, ya: int, xb: int, yb: int, color: tuple[int, int, int]) -> None:
        dx = abs(xb - xa)
        sx = 1 if xa < xb else -1
        dy = -abs(yb - ya)
        sy = 1 if ya < yb else -1
        err = dx + dy
        x, y = xa, ya
        while True:
            if 0 <= x < width and 0 <= y < height:
                pixels[y][x] = color
            if x == xb and y == yb:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    for (xa, ya), (xb, yb) in zip(points[:-1], points[1:], strict=False):
        draw_line(xa, ya, xb, yb, blue)

    for x, y in points:
        for oy in range(-3, 4):
            for ox in range(-3, 4):
                if ox * ox + oy * oy <= 9:
                    xx = x + ox
                    yy = y + oy
                    if 0 <= xx < width and 0 <= yy < height:
                        pixels[yy][xx] = blue

    _write_png(plot_path, width, height, pixels)




def _draw_scaling_svg(
    plot_path: Path,
    epsilon_values: list[float],
    perimeter_values: list[float],
    delineation_label: str,
    fit_slope: float,
) -> None:
    """Draw a publication-style SVG line plot for website display."""
    width, height = 980, 620
    margin_left, margin_right = 120, 50
    margin_top, margin_bottom = 95, 95

    x0, x1 = margin_left, width - margin_right
    y0, y1 = margin_top, height - margin_bottom

    xmin, xmax = min(epsilon_values), max(epsilon_values)
    ymin, ymax = min(perimeter_values), max(perimeter_values)
    ypad = (ymax - ymin) * 0.05 if ymax > ymin else 1.0
    ymin -= ypad
    ymax += ypad

    def to_xy(xv: float, yv: float) -> tuple[float, float]:
        xn = 0.0 if xmax == xmin else (xv - xmin) / (xmax - xmin)
        yn = 0.0 if ymax == ymin else (yv - ymin) / (ymax - ymin)
        px = x0 + xn * (x1 - x0)
        py = y1 - yn * (y1 - y0)
        return px, py

    points = [to_xy(xv, yv) for xv, yv in zip(epsilon_values, perimeter_values, strict=False)]
    polyline = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)

    x_ticks = [xmin + (xmax - xmin) * i / 5 for i in range(6)]
    y_ticks = [ymin + (ymax - ymin) * i / 4 for i in range(5)]

    def _fmt_tick(value: float) -> str:
        if abs(value) >= 100:
            return f"{value:.0f}"
        if abs(value) >= 10:
            return f"{value:.1f}"
        return f"{value:.2f}"

    grid_h = "\n".join(
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#e1e1e1" stroke-width="1" />'
        for y in (y0 + (y1 - y0) * i / 4 for i in range(5))
    )
    grid_v = "\n".join(
        f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="#e1e1e1" stroke-width="1" />'
        for x in (x0 + (x1 - x0) * i / 5 for i in range(6))
    )
    dots = "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.8" fill="#234A65" />' for x, y in points
    )
    x_tick_labels = "\n".join(
        (
            f'<text x="{to_xy(tick, ymin)[0]:.2f}" y="{y1 + 32}" text-anchor="middle" '
            f'font-size="15" fill="#334">{_fmt_tick(tick)}</text>'
        )
        for tick in x_ticks
    )
    y_tick_labels = "\n".join(
        (
            f'<text x="{x0 - 14}" y="{to_xy(xmin, tick)[1] + 5:.2f}" text-anchor="end" '
            f'font-size="15" fill="#334">{_fmt_tick(tick)}</text>'
        )
        for tick in y_ticks
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Synthetic WUI boundary scaling plot">
  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff" />
  <text x="{x0}" y="42" font-size="30" font-weight="700" fill="#234A65">Synthetic WUI boundary scaling demo</text>
  <text x="{x0}" y="68" font-size="16" fill="#445">Boundary length decreases slightly as epsilon gets coarser in this synthetic run.</text>
  {grid_h}
  {grid_v}
  <line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#505050" stroke-width="1.5" />
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#505050" stroke-width="1.5" />
  {x_tick_labels}
  {y_tick_labels}
  <polyline fill="none" stroke="#234A65" stroke-width="2.8" points="{polyline}" />
  {dots}
  <text x="{(x0 + x1) / 2:.2f}" y="{height - 38}" text-anchor="middle" font-size="17" fill="#1f2e38">Measurement scale, epsilon (effective ruler length / resolution)</text>
  <text x="32" y="{(y0 + y1) / 2:.2f}" text-anchor="middle" font-size="17" fill="#1f2e38" transform="rotate(-90 32 {(y0 + y1) / 2:.2f})">Measured boundary length, L_d(epsilon)</text>
  <rect x="{x0 + 18}" y="{y0 + 16}" width="470" height="74" fill="#ffffff" opacity="0.96" stroke="#d9dee2" rx="8" />
  <line x1="{x0 + 32}" y1="{y0 + 43}" x2="{x0 + 86}" y2="{y0 + 43}" stroke="#234A65" stroke-width="2.8" />
  <circle cx="{x0 + 59}" cy="{y0 + 43}" r="4" fill="#234A65" />
  <text x="{x0 + 96}" y="{y0 + 48}" font-size="14" fill="#233">Synthetic delineation: {delineation_label}</text>
  <text x="{x0 + 32}" y="{y0 + 72}" font-size="14" fill="#233">Log-log slope estimate: {fit_slope:.4f}; evaluated scales: {len(epsilon_values)}</text>
</svg>
"""
    plot_path.write_text(svg, encoding="utf-8")

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI options for the synthetic demo run."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-subdir",
        default="minimal_demo",
        help="Directory name under outputs/ for generated files (default: minimal_demo)",
    )
    parser.add_argument("--min-epsilon", type=float, default=1.0, help="Minimum epsilon value")
    parser.add_argument("--max-epsilon", type=float, default=30.0, help="Maximum epsilon value")
    parser.add_argument("--n-steps", type=int, default=8, help="Number of epsilon grid steps")
    parser.add_argument(
        "--vegetation-threshold",
        type=float,
        default=0.35,
        help="Synthetic delineation vegetation threshold",
    )
    parser.add_argument(
        "--neighborhood-radius-m",
        type=float,
        default=120.0,
        help="Synthetic delineation neighborhood radius in meters",
    )
    parser.add_argument(
        "--adjacency-rule",
        default="touches",
        help="Synthetic delineation adjacency rule label",
    )
    parser.add_argument(
        "--skip-doc-publish",
        action="store_true",
        help="Do not copy outputs into docs/assets (useful for local experiments)",
    )
    parser.add_argument(
        "--include-satellite-demo",
        action="store_true",
        help="Also generate satellite-like resolution scaling outputs and docs assets.",
    )
    return parser.parse_args(argv)


def _draw_satellite_scaling_svg(
    plot_path: Path,
    epsilon_values: list[float],
    perimeter_values: list[float],
    fit_slope: float | None,
    fit_intercept: float | None,
) -> None:
    """Draw a publication-style SVG for satellite-like measurement scales."""
    width, height = 980, 620
    margin_left, margin_right = 120, 55
    margin_top, margin_bottom = 98, 95

    x0, x1 = margin_left, width - margin_right
    y0, y1 = margin_top, height - margin_bottom

    xmin, xmax = min(epsilon_values), max(epsilon_values)
    ymin, ymax = min(perimeter_values), max(perimeter_values)
    ypad = (ymax - ymin) * 0.09 if ymax > ymin else 1.0
    ymin -= ypad
    ymax += ypad

    def to_xy(xv: float, yv: float) -> tuple[float, float]:
        xn = 0.0 if xmax == xmin else (xv - xmin) / (xmax - xmin)
        yn = 0.0 if ymax == ymin else (yv - ymin) / (ymax - ymin)
        px = x0 + xn * (x1 - x0)
        py = y1 - yn * (y1 - y0)
        return px, py

    points = [to_xy(xv, yv) for xv, yv in zip(epsilon_values, perimeter_values, strict=False)]
    polyline = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)

    def _fmt_y(value: float) -> str:
        if abs(value) >= 100:
            return f"{value:.0f}"
        return f"{value:.1f}"

    y_ticks = [ymin + (ymax - ymin) * i / 4 for i in range(5)]
    grid_h = "\n".join(
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#e1e1e1" stroke-width="1" />'
        for y in (y0 + (y1 - y0) * i / 4 for i in range(5))
    )
    grid_v = "\n".join(
        f'<line x1="{to_xy(scale, ymin)[0]:.2f}" y1="{y0}" x2="{to_xy(scale, ymin)[0]:.2f}" y2="{y1}" stroke="#e1e1e1" stroke-width="1" />'
        for scale in epsilon_values
    )
    dots = "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.2" fill="#234A65" />' for x, y in points
    )
    x_tick_labels = "\n".join(
        (
            f'<text x="{to_xy(scale, ymin)[0]:.2f}" y="{y1 + 32}" text-anchor="middle" '
            f'font-size="14" fill="#334">{int(scale)} m</text>'
        )
        for scale in epsilon_values
    )
    y_tick_labels = "\n".join(
        (
            f'<text x="{x0 - 14}" y="{to_xy(xmin, tick)[1] + 5:.2f}" text-anchor="end" '
            f'font-size="15" fill="#334">{_fmt_y(tick)}</text>'
        )
        for tick in y_ticks
    )

    fit_text = (
        f"log-log fit slope = {fit_slope:.4f}, intercept = {fit_intercept:.4f}"
        if fit_slope is not None and fit_intercept is not None
        else "log-log fit unavailable for this synthetic run"
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Satellite-like resolution scaling plot for synthetic WUI boundary">
  <rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff" />
  <text x="{x0}" y="42" font-size="30" font-weight="700" fill="#234A65">Synthetic satellite-like resolution scaling</text>
  <text x="{x0}" y="68" font-size="16" fill="#445">Coarser pixel sizes act like larger rulers and smooth measured perimeter.</text>
  {grid_h}
  {grid_v}
  <line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#505050" stroke-width="1.5" />
  <line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#505050" stroke-width="1.5" />
  {x_tick_labels}
  {y_tick_labels}
  <polyline fill="none" stroke="#234A65" stroke-width="2.9" points="{polyline}" />
  {dots}
  <text x="{(x0 + x1) / 2:.2f}" y="{height - 38}" text-anchor="middle" font-size="17" fill="#1f2e38">Satellite-like measurement scale / pixel size (meters)</text>
  <text x="32" y="{(y0 + y1) / 2:.2f}" text-anchor="middle" font-size="17" fill="#1f2e38" transform="rotate(-90 32 {(y0 + y1) / 2:.2f})">Measured synthetic boundary length, L_d(epsilon)</text>
  <rect x="{x0 + 20}" y="{y0 + 18}" width="610" height="92" fill="#ffffff" opacity="0.96" stroke="#d9dee2" rx="8" />
  <text x="{x0 + 34}" y="{y0 + 48}" font-size="14" fill="#233">Synthetic demonstration only (not empirical satellite inference).</text>
  <text x="{x0 + 34}" y="{y0 + 72}" font-size="14" fill="#233">{fit_text}</text>
  <text x="{x0 + 34}" y="{y0 + 95}" font-size="14" fill="#233">Finer scales resolve more irregularity; coarser scales shorten apparent interface.</text>
</svg>
"""
    plot_path.write_text(svg, encoding="utf-8")


def run(args: argparse.Namespace | None = None) -> None:
    if args is None:
        args = parse_args()

    output_dir = ROOT / "outputs" / args.output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)
    docs_figure_dir = ROOT / "docs" / "assets" / "figures"
    docs_data_dir = ROOT / "docs" / "assets" / "data"
    if not args.skip_doc_publish:
        docs_figure_dir.mkdir(parents=True, exist_ok=True)
        docs_data_dir.mkdir(parents=True, exist_ok=True)

    bundle = DelineationBundle(
        settlement_representation="parcel",
        vegetation_threshold=args.vegetation_threshold,
        neighborhood_radius_m=args.neighborhood_radius_m,
        adjacency_rule=args.adjacency_rule,
    )
    boundary = synthetic_boundary_from_delineation(bundle)
    epsilon_values = validate_scale_grid(
        ScaleGrid(min_epsilon=args.min_epsilon, max_epsilon=args.max_epsilon, n_steps=args.n_steps)
    )

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

    plot_path = output_dir / "boundary_scaling_plot.png"
    _draw_scaling_plot(plot_path, measurement["epsilon_values"], measurement["perimeter_values"])

    plot_svg_path = output_dir / "boundary_scaling_plot.svg"
    _draw_scaling_svg(
        plot_svg_path,
        measurement["epsilon_values"],
        measurement["perimeter_values"],
        bundle.short_id(),
        fit.slope,
    )

    docs_plot_path = docs_figure_dir / "boundary_scaling_plot.svg"
    docs_csv_path = docs_data_dir / "boundary_scaling_summary.csv"
    satellite_csv_path: Path | None = None
    satellite_png_path: Path | None = None
    satellite_svg_path: Path | None = None
    if not args.skip_doc_publish:
        shutil.copy2(plot_svg_path, docs_plot_path)
        shutil.copy2(table_path, docs_csv_path)

    if args.include_satellite_demo:
        satellite_scales = [1.0, 10.0, 30.0, 100.0, 250.0, 500.0]
        satellite_measurement = measure_perimeter_over_scales_toy(
            boundary_points=boundary,
            epsilon_values=satellite_scales,
            boundary_object_id="synthetic_wui_boundary_001",
            base_resolution=1.0,
        )
        satellite_fit = fit_loglog_scaling(
            satellite_measurement["epsilon_values"],
            satellite_measurement["perimeter_values"],
        )

        satellite_csv_path = output_dir / "satellite_resolution_scaling_summary.csv"
        with satellite_csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "delineation_id",
                    "boundary_object_id",
                    "measurement_scale_m",
                    "perimeter",
                    "fit_status",
                    "loglog_slope",
                    "loglog_intercept",
                    "n_scales",
                ],
            )
            writer.writeheader()
            for epsilon, perimeter in zip(
                satellite_measurement["epsilon_values"],
                satellite_measurement["perimeter_values"],
                strict=False,
            ):
                writer.writerow(
                    {
                        "delineation_id": summary_row["delineation_id"],
                        "boundary_object_id": satellite_measurement["boundary_object_id"],
                        "measurement_scale_m": epsilon,
                        "perimeter": perimeter,
                        "fit_status": satellite_fit.status,
                        "loglog_slope": satellite_fit.slope,
                        "loglog_intercept": satellite_fit.intercept,
                        "n_scales": len(satellite_measurement["epsilon_values"]),
                    }
                )

        satellite_png_path = output_dir / "satellite_resolution_scaling_plot.png"
        _draw_scaling_plot(
            satellite_png_path,
            satellite_measurement["epsilon_values"],
            satellite_measurement["perimeter_values"],
        )

        satellite_svg_path = output_dir / "satellite_resolution_scaling_plot.svg"
        _draw_satellite_scaling_svg(
            satellite_svg_path,
            satellite_measurement["epsilon_values"],
            satellite_measurement["perimeter_values"],
            satellite_fit.slope,
            satellite_fit.intercept,
        )

        if not args.skip_doc_publish:
            shutil.copy2(satellite_svg_path, docs_figure_dir / "satellite_resolution_scaling_plot.svg")
            shutil.copy2(satellite_csv_path, docs_data_dir / "satellite_resolution_scaling_summary.csv")

    summary_lines = [
        "# Minimal boundary scaling demo summary",
        "",
        "This run is synthetic and intended only to demonstrate executability.",
        f"- delineation bundle d: `{bundle.label()}`",
        f"- boundary object id: `{measurement['boundary_object_id']}`",
        f"- epsilon grid size: {len(measurement['epsilon_values'])}",
        (
            "- epsilon range: "
            f"{measurement['epsilon_values'][0]} to {measurement['epsilon_values'][-1]} "
            f"({len(measurement['epsilon_values'])} steps)"
        ),
        f"- scaling fit status: `{fit.status}`",
        f"- estimated log-log slope: `{fit.slope}`",
        f"- docs publish step: {'skipped' if args.skip_doc_publish else 'enabled'}",
        f"- satellite-like resolution demo: {'enabled' if args.include_satellite_demo else 'disabled'}",
    ]
    write_markdown_summary(output_dir / "run_summary.md", summary_lines)

    print(f"Wrote: {table_path}")
    print(f"Wrote: {plot_path}")
    print(f"Wrote: {plot_svg_path}")
    if satellite_csv_path is not None and satellite_png_path is not None and satellite_svg_path is not None:
        print(f"Wrote: {satellite_csv_path}")
        print(f"Wrote: {satellite_png_path}")
        print(f"Wrote: {satellite_svg_path}")
    if args.skip_doc_publish:
        print("Skipped docs asset publish (--skip-doc-publish).")
    else:
        print(f"Published: {docs_csv_path}")
        print(f"Published: {docs_plot_path}")
        if args.include_satellite_demo:
            print(f"Published: {docs_data_dir / 'satellite_resolution_scaling_summary.csv'}")
            print(f"Published: {docs_figure_dir / 'satellite_resolution_scaling_plot.svg'}")
    print(f"Wrote: {output_dir / 'run_summary.md'}")


if __name__ == "__main__":
    run(parse_args())

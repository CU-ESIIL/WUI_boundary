#!/usr/bin/env python3
"""Run minimal streaming ESA WorldCover + OSM building interface scaling demo."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from boundary_analytics.streaming_wui import run_streaming_demo


def _parse_bbox(value: str) -> tuple[float, float, float, float]:
    values = [float(v.strip()) for v in value.split(",")]
    if len(values) != 4:
        raise ValueError("bbox must be minx,miny,maxx,maxy")
    return values[0], values[1], values[2], values[3]


def _parse_int_list(value: str) -> list[int]:
    return [int(v.strip()) for v in value.split(",") if v.strip()]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bbox", default="-105.271,40.018,-105.268,40.021")
    parser.add_argument("--outdir", default="outputs/real_data_demo")
    parser.add_argument("--resolutions", default="10,20,40,80")
    parser.add_argument("--adj-buffer", type=float, default=30.0)
    parser.add_argument("--publish-doc-assets", action="store_true")
    return parser.parse_args(argv)


def _publish_outputs(outdir: Path) -> None:
    docs_data = ROOT / "docs" / "assets" / "data"
    docs_fig = ROOT / "docs" / "assets" / "figures"
    docs_data.mkdir(parents=True, exist_ok=True)
    docs_fig.mkdir(parents=True, exist_ok=True)
    shutil.copy2(outdir / "interface_scaling.csv", docs_data / "real_interface_scaling.csv")
    shutil.copy2(outdir / "interface_scaling.png", docs_fig / "real_interface_scaling.png")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    outdir = ROOT / args.outdir
    run_streaming_demo(
        bbox=_parse_bbox(args.bbox),
        outdir=outdir,
        target_resolutions_m=_parse_int_list(args.resolutions),
        adj_buffer_m=args.adj_buffer,
    )
    if args.publish_doc_assets:
        _publish_outputs(outdir)
    print(f"Wrote outputs to {outdir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

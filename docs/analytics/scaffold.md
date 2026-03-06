# Boundary Analytics Scaffold

The Boundary Analytics scaffold is a lightweight Python package skeleton for reproducible estimation of scale-conditioned WUI boundary length, \(L_d(\varepsilon)\).

## Purpose

Provide stable interfaces for moving from a conceptual UI prototype to executable analytics while being explicit about what is synthetic versus real.

## Current status

Implemented now:

- Typed configuration objects for delineation bundles (`d`) and scale-grid settings (`epsilon`).
- A synthetic boundary fixture generator tied to delineation bundle settings.
- A toy perimeter measurement function over epsilon grids.
- A minimal log-log scaling helper with diagnostics and graceful insufficient-point handling.
- A runnable script: `scripts/run_minimal_boundary_scaling.py`.
- Minimal tests for config validation, measurement outputs, scaling behavior, and placeholders.

Not implemented yet:

- Real geospatial boundary delineation from empirical settlement + vegetation data.
- Real perimeter measurement from vector/raster geometry products.
- Multi-study-area calibration and uncertainty analysis.

## Scientific framing preserved

- **Definition scale** remains represented by delineation bundle index `d`.
- **Measurement scale** remains represented by `epsilon` in perimeter measurement.
- The central object remains `L_d(epsilon)`.

The current runner intentionally demonstrates this on synthetic geometry only.

## Re-run steps

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_minimal_boundary_scaling.py
```

Expected output location:

- `outputs/minimal_demo/boundary_scaling_plot.png`
- `outputs/minimal_demo/boundary_scaling_summary.csv`
- `outputs/minimal_demo/run_summary.md`

## Future real-data inputs (expected)

- Settlement and vegetation layers (with provenance and licensing metadata).
- Study-area boundary definitions.
- Datasets or services needed to evaluate delineation bundles \(d\).
- Scale-grid specification for measurement scales \(\varepsilon\).

## Expected outputs later

- Perimeter-by-scale tables for each delineation bundle: \(L_d(\varepsilon)\).
- Model fit summaries and diagnostics.
- Figure-ready data products for manuscript and site publication.

See [UI Drafts / Draft 1](../ui-drafts/draft-1.md) for the current story-lab interface and [Roadmap to Real Data](../ui-drafts/roadmap-to-real-data.md) for planned implementation steps.

## Automation

GitHub Actions workflow `.github/workflows/boundary-scaling-demo.yml` runs tests, executes the synthetic minimal demo, uploads `outputs/minimal_demo/` as artifacts, and refreshes selected docs-facing assets for website publication.

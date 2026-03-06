# Boundary Analytics Scaffold

The Boundary Analytics scaffold is a lightweight Python package skeleton for future reproducible estimation of scale-conditioned WUI boundary length, \(L_d(\varepsilon)\).

## Purpose

Provide stable interfaces for moving from a conceptual UI prototype to real-data analytics without over-claiming current capability.

## Current status

Implemented now:

- Typed configuration objects for delineation bundles and scale-grid settings.
- Function interfaces and structured placeholder outputs for measurement, scaling diagnostics, data loading, and reporting.
- Minimal tests for object construction, validation, and output structure.

Not implemented yet:

- Real geospatial boundary delineation.
- Real perimeter measurement from spatial data.
- Real log-log model estimation over observed datasets.

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

# Scaling results

This page shows the current **synthetic demo** outputs for scale-conditioned boundary length,
\(L_d(\varepsilon)\), in a website-ready format.

!!! warning "Synthetic demo"
    The outputs shown here are generated from synthetic data and toy geometry. They demonstrate analysis wiring and interpretation logic, not empirical WUI estimates.

!!! info "How results reach this website"
    - **Pull request runs** create artifacts for validation and review.
    - **Manual publish runs** regenerate and publish website-facing assets.
    - **Local runs** write to `outputs/` and only affect the website after assets are copied into `docs/assets/` and published.

## Current scaling plot

<div
  id="scaling-summary-plot"
  class="scaling-plot-wrap"
  data-csv-plot="true"
  data-csv-src="../assets/data/boundary_scaling_summary.csv"
  data-csv-fallback="Scaling plot is unavailable right now. You can still download the CSV below.">
  Loading scaling plot…
</div>

The synthetic demo shows measured perimeter changing across the tested scale grid, which is exactly why boundary length should be reported as a function of scale rather than a single constant.

## Summary table (rendered from CSV)

<div
  id="scaling-summary-table"
  class="scaling-table-wrap"
  data-csv-table="true"
  data-csv-src="../assets/data/boundary_scaling_summary.csv"
  data-csv-fallback="Summary table is unavailable right now. You can still download the CSV below.">
  Loading summary table…
</div>

[Download summary CSV](assets/data/boundary_scaling_summary.csv)

## Reading the scaling relationship

For a fixed delineation choice \(d\), we evaluate \(L_d(\varepsilon)\) over a grid of measurement scales \(\varepsilon\). A common summary is a log-log relationship:
\[
\log L_d(\varepsilon) = a_d + b_d\log(\varepsilon),
\]
where the slope \(b_d\) quantifies how rapidly measured length changes with scale.

In plain terms:

- a steeper magnitude of slope means stronger scale sensitivity;
- a flatter slope means weaker sensitivity over the tested scale range.

## Typical workflows

1. **Local experimentation:** run analysis locally, inspect `outputs/minimal_demo/`, and iterate quickly.
2. **Pull request validation:** open a PR and use run artifacts to review outputs before publishing.
3. **Manual publish to website:** trigger a manual publish run to refresh `docs/assets/` and update the live page.

## Interpretation guardrails

The scientific point is not the synthetic slope value itself. The key result is structural: boundary length should be interpreted as a function of both delineation and scale, \(L_d(\varepsilon)\), rather than a single perimeter constant.

[Next: Fire science implications](fire-science-implications.md){ .md-button .md-button--primary }

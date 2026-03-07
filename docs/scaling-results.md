# Scaling results

This section summarizes the current reproducible demonstration of scale-conditioned boundary length using
\[
L_d(\varepsilon).
\]

!!! warning "Synthetic demo"
    The outputs shown here are generated from synthetic data and toy geometry. They demonstrate analysis wiring and interpretation logic, not empirical WUI estimates.

## Reading the scaling relationship

For a fixed delineation choice \(d\), we evaluate \(L_d(\varepsilon)\) over a grid of measurement scales \(\varepsilon\). A common summary is a log-log relationship:
\[
\log L_d(\varepsilon) = a_d + b_d\log(\varepsilon),
\]
where the slope \(b_d\) quantifies how rapidly measured length changes with scale.

In plain terms:

- a steeper magnitude of slope means stronger scale sensitivity;
- a flatter slope means weaker sensitivity over the tested scale range.

## Current figure

<img src="assets/figures/boundary_scaling_plot.png" alt="Synthetic WUI boundary scaling relationship" loading="lazy" />

If this image is missing in a fresh checkout, regenerate it using the methods page workflow.

## Current summary table

The companion summary table is published at:

- [`docs/assets/data/boundary_scaling_summary.csv`](assets/data/boundary_scaling_summary.csv)

## Interpretation guardrails

The scientific point is not the synthetic slope value itself. The key result is structural: boundary length should be interpreted as a function of both delineation and scale, \(L_d(\varepsilon)\), rather than a single perimeter constant.

[Next: Fire science implications](fire-science-implications.md){ .md-button .md-button--primary }

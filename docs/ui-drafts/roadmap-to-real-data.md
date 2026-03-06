# Roadmap to Real Data

Draft 1 demonstrates the logic of scale-conditioned boundary length. This roadmap describes how that conceptual interface transitions to reproducible, real-data analytics.

## Planned scientific workflow

1. **Define WUI boundaries under multiple delineation bundles** \(d\), using defensible combinations of settlement representation, vegetation threshold, neighborhood radius, and adjacency rules.
2. **Measure perimeter over a scale grid** \(\varepsilon\), so each delineation bundle yields a curve \(L_d(\varepsilon)\).
3. **Fit and diagnose log-log scaling relationships** for each \(d\), including model diagnostics rather than slope-only summaries.
4. **Compare sensitivity partitions** between definition-scale choices and measurement-scale choices.
5. **Test across multiple study areas** to assess transferability and context dependence.
6. **Export manuscript-ready tables and figures** and site-ready summary artifacts from the same reproducible pipeline.

## Status: now vs scaffolded vs not yet implemented

### Already in this repository now

- A website-integrated, presentation-ready Draft 1 story lab for conceptual communication.
- Documentation that explicitly distinguishes object-definition scale and measurement scale.

### Scaffolded now

- A lightweight analytics package structure with typed configuration objects and function interfaces for definitions, measurement, scaling, dataset I/O, and reporting.
- Basic tests that validate argument handling and structured placeholder outputs.

### Still requires real-data implementation

- Real geospatial input datasets and documented data-access methods.
- Operational delineation and perimeter algorithms on spatial layers.
- Production model fitting, diagnostics, multi-area benchmarking, and publication-grade result generation.

See [Draft 1 — WUI Boundary Story Lab](draft-1.md) for the current interface and [Boundary Analytics Scaffold](../analytics/scaffold.md) for code-level scaffolding.

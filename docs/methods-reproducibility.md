# Methods & reproducibility

This page reframes the implementation status as an analysis framework for a living manuscript.

## Study design overview

The intended empirical workflow is:

1. define multiple delineation bundles \(d\) for what counts as WUI boundary,
2. measure perimeter over a scale grid \(\varepsilon\),
3. estimate and diagnose scaling relationships,
4. compare sensitivity partitions across \(d\) and \(\varepsilon\),
5. publish figure- and table-ready outputs.

## Current status

!!! info "Status labels"
    - **Conceptual:** interactive Story Lab interfaces for scientific communication.  
    - **Synthetic demo:** executable minimal analysis in the repository today.  
    - **Empirical workflow target:** real-data delineation and measurement pipeline.

Implemented now:

- analytics scaffold package in `src/boundary_analytics` for definitions, measurement, scaling, datasets, and reporting,
- synthetic minimal runner `scripts/run_minimal_boundary_scaling.py`,
- tests validating scaffold behavior in `tests/test_scaffold.py`,
- docs-facing synthetic outputs (CSV and generated figure paths).

Not yet implemented:

- empirical dataset ingestion with provenance/licensing metadata,
- production delineation and perimeter algorithms on real geospatial layers,
- multi-area calibration and uncertainty-aware benchmarking.

## Repository structure (analysis-relevant)

- `src/boundary_analytics/` — scaffolded analysis interfaces and toy implementations.
- `scripts/run_minimal_boundary_scaling.py` — reproducible synthetic run.
- `tests/test_scaffold.py` — minimal behavior checks.
- `outputs/minimal_demo/` — run outputs.
- `docs/assets/data/` and `docs/assets/figures/` — published docs-facing artifacts.

## Reproduce the current synthetic run

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_minimal_boundary_scaling.py
```

Expected outputs:

- `outputs/minimal_demo/boundary_scaling_plot.png`
- `outputs/minimal_demo/boundary_scaling_summary.csv`
- `outputs/minimal_demo/run_summary.md`
- `docs/assets/figures/boundary_scaling_plot.png`
- `docs/assets/data/boundary_scaling_summary.csv`

## Forward path to empirical analysis

The next step is not a redesign of the conceptual claim; it is empirical activation of the same \(L_d(\varepsilon)\) framework with transparent data provenance, reproducible preprocessing, and explicit uncertainty reporting.

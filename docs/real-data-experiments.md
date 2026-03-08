# Real-data experiments

The analytical framework developed in this project begins with synthetic geometry because synthetic boundaries make the logic of L_d(epsilon) easier to see. They allow the distinction between delineation choice and measurement scale to be introduced without the additional complexity of heterogeneous real landscapes, imperfect classifications, and mixed-resolution data products. But the scientific motivation of the project ultimately points beyond toy geometry. The question is not only whether synthetic boundaries exhibit scale dependence. It is whether remotely sensed representations of the Wildland–Urban Interface do so as well.

For that reason the next phase of the project is a deliberately modest transition into real data. The aim is not yet to build a complete continental WUI product. It is to establish a small, transparent pathway through which settlement data and vegetation data can be brought into the same analytical frame, converted into a boundary object, and measured across multiple effective scales.

This page documents that transition. The current implementation is still a scaffold, but it clarifies the structure of the empirical workflow to come: acquisition, clipping, preprocessing, boundary construction, perimeter measurement, and scaling analysis. In that sense it belongs to the same argument as the synthetic work. The goal remains the same. What changes is the nature of the object being measured.

## Current scaffold implementation

The repository now includes a three-step prototype pipeline under `scripts/`: `download_sample_data.py`, `build_sample_wui_boundary.py`, and `run_real_boundary_scaling.py`. Together they define a reproducible handoff from acquisition metadata to a processed boundary artifact and then to scale-dependent perimeter summaries.

The expected on-disk structure is `data/raw/<region_id>/` for source files and `data/processed/<region_id>/` for derived boundary products and run metadata. This keeps externally sourced inputs separate from pipeline-generated intermediates while making the region scope explicit.

At this stage, the scaffold is intentionally mixed between implemented and stubbed behavior. Region configuration, dataset manifests, boundary-prototype outputs, and scaling execution wiring are implemented. Provider-specific download details, exact settlement-vegetation overlay logic, and production-quality boundary extraction are still stubbed and clearly marked for follow-on empirical development.

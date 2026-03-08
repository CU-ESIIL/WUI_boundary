# Real-data experiments

The analytical framework developed in this project begins with synthetic geometry because synthetic boundaries make the logic of \(L_d(\varepsilon)\) easier to see. They allow the distinction between delineation choice and measurement scale to be introduced without the additional complexity of heterogeneous real landscapes, imperfect classifications, and mixed-resolution data products. But the scientific motivation of the project ultimately points beyond toy geometry. The question is not only whether synthetic boundaries exhibit scale dependence. It is whether remotely sensed representations of the Wildland–Urban Interface do so as well.

For that reason the next phase of the project is a deliberately modest transition into real data. The aim is not yet to build a complete continental WUI product. It is to establish a small, transparent pathway through which settlement data and vegetation data can be brought into the same analytical frame, converted into a boundary object, and measured across multiple effective scales.

This page documents that transition. The current implementation is still a scaffold, but it clarifies the structure of the empirical workflow to come: acquisition, clipping, preprocessing, boundary construction, perimeter measurement, and scaling analysis. In that sense it belongs to the same argument as the synthetic work. The goal remains the same. What changes is the nature of the object being measured.

The pilot now uses an open, no-keys workflow centered on two public sources: OpenStreetMap building footprints queried from Overpass for settlement structure, and a streamed NLCD raster window for vegetation classes. The objective is to build a first empirical settlement–vegetation interface and evaluate how its measured length behaves under explicit scale changes. This implementation is intentionally modest, transparent, and reproducible in a normal networked environment.

The underlying runner is `scripts/run_streaming_wui_scaling.py`. It accepts a small lon/lat bounding box, constructs a WUI-like interface, and writes figure and table outputs for publication. Buildings are unioned into a settlement object. Selected NLCD classes are unioned into a vegetation object. The reported interface corresponds to vegetation boundary segments that fall within a configurable settlement buffer. This is a first empirical pilot designed to test geometry and scale logic; it is not a final official WUI mapping product.

## Experiment A: fixed-boundary measurement-scale test

In the first experiment, the empirical interface is held fixed and measured at multiple effective ruler lengths \(\varepsilon\). This isolates measurement-scale sensitivity for one delineation choice. If finer \(\varepsilon\) values resolve additional edge irregularity, measured length should increase accordingly.

<img src="/WUI_boundary/assets/figures/real_fixed_boundary_scaling.png" alt="Fixed-boundary measurement-scale experiment for the real-data pilot" loading="lazy" class="scaling-results-plot" />

*Figure. Fixed-boundary measurement-scale experiment for the empirical pilot. The geometry is held constant while measurement scale is varied, so the curve reflects scale-conditioned measurement behavior for one settlement–vegetation interface object.*

The associated data table is published at [`docs/assets/data/real_fixed_boundary_scaling.csv`](/WUI_boundary/assets/data/real_fixed_boundary_scaling.csv).

## Experiment B: resolution-rebuild test

In the second experiment, the vegetation side is rebuilt from progressively coarser raster resolutions, and the settlement–vegetation interface is reconstructed and remeasured each time. This introduces a scientifically meaningful blend of object-definition and observational-scale effects, approximating how different raster grain choices can alter measured interface length.

<img src="/WUI_boundary/assets/figures/real_resolution_rebuild_scaling.png" alt="Resolution-rebuild experiment for the real-data pilot" loading="lazy" class="scaling-results-plot" />

*Figure. Resolution-rebuild experiment for the empirical pilot. As vegetation raster grain is coarsened and geometry is rebuilt, measured interface length tracks the combined effect of observational scale and raster-conditioned boundary reconstruction.*

The associated data table is published at [`docs/assets/data/real_resolution_rebuild_scaling.csv`](/WUI_boundary/assets/data/real_resolution_rebuild_scaling.csv).

These two experiments provide a concrete bridge from synthetic demonstrations to empirical boundary measurement using open, keyless data access. They should be read as a first reproducible pilot and a method-development scaffold, not as a final national WUI product.

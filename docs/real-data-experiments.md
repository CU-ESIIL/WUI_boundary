# Real-data experiments

The analytical framework developed in this project begins with synthetic geometry because synthetic boundaries make the logic of \(L_d(\varepsilon)\) easier to see. They allow the distinction between delineation choice and measurement scale to be introduced without the additional complexity of heterogeneous real landscapes, imperfect classifications, and mixed-resolution data products. But the scientific motivation of the project ultimately points beyond toy geometry. The question is not only whether synthetic boundaries exhibit scale dependence. It is whether remotely sensed representations of the Wildland–Urban Interface do so as well.

For that reason the next phase of the project is a deliberately modest transition into real data. The aim is not yet to build a complete continental WUI product. It is to establish a small, transparent pathway through which settlement data and vegetation data can be brought into the same analytical frame, converted into a boundary object, and measured across multiple effective scales.

The pilot now uses an open, no-keys workflow centered on two public sources: OpenStreetMap building footprints queried from Overpass for settlement structure, and a streamed ESA WorldCover COG window for vegetation classes. The objective is to build a first empirical settlement–vegetation interface and evaluate how its measured length behaves under explicit scale changes. This implementation is intentionally small, deterministic, and CI-friendly.

The runner is `scripts/run_streaming_wui_scaling.py`. It accepts a tiny lon/lat bounding box, streams only that raster window from the ESA WorldCover COG, unions OSM buildings into settlement geometry, converts vegetation mask cells into polygons, coarsens the mask by integer factors with majority rule, and fits a log-log relationship between interface length and effective resolution.

## Streaming demo output

A successful run writes:

- `outputs/real_data_demo/interface_scaling.csv`
- `outputs/real_data_demo/interface_scaling.json`
- `outputs/real_data_demo/interface_scaling.png`

With `--publish-doc-assets`, website-facing copies are written to:

- `docs/assets/data/real_interface_scaling.csv`
- `docs/assets/figures/real_interface_scaling.png`

This pilot should be read as a method-development bridge from synthetic demonstrations to empirical boundary measurement using open, keyless data access, not as a final official WUI product.

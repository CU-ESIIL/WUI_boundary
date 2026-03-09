# Methods & reproducibility

The current analytical pipeline is a deliberately simplified scaffold for testing the logic of \(L_d(\varepsilon)\) before empirical WUI datasets are brought fully into the workflow. Rather than treating synthetic output as a substitute for real landscape analysis, the pipeline uses toy geometry to make the structure of the problem explicit and reproducible.

This matters because the core claim of the project is methodological as much as geometric. Boundary length must be interpreted in relation to how the boundary object was defined and how the measurement scale was chosen. A small, transparent, synthetic pipeline is therefore useful not because it resolves the empirical question, but because it demonstrates the analytical wiring needed to ask that question clearly.

What follows documents the current execution pathway, the published outputs, and the local and continuous-integration routes through which figures and summary data are regenerated. The purpose of this page is practical, but it should be read in continuity with the rest of the site: reproducibility here serves interpretation, not just software maintenance.

Install dependencies and run baseline checks:

```bash
python -m pip install -e .
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_minimal_boundary_scaling.py --include-satellite-demo
```

The canonical install path for contributors and CI runtime is `python -m pip install -e .`. This installs the geospatial stack needed by the streaming pilot (`geopandas`, `rasterio`, `shapely`, `pyproj`, `pyogrio`, `numpy`, `pandas`, `matplotlib`, `requests`, and `scipy`). `requirements.txt` is documentation-only (MkDocs) and should be layered on top when you need local site builds.

Run the website validation gate for docs and UI-facing changes:

```bash
scripts/pre_pr_site_review.sh
```

## Streaming real-data pilot (OSM + NLCD, no keys)

The repository now includes `scripts/run_streaming_wui_scaling.py`, a first empirical WUI-like pilot that pairs OSM building footprints (Overpass API) with a streamed NLCD raster subset. The workflow requires network access but no API keys or secrets. For CI and constrained runners, keep network retries bounded (`--network-timeout-s`, `--max-network-attempts`) so failures are explicit rather than ending as long-running cancellations. In GitHub Actions, pull requests run the lightweight synthetic validation path. The networked streaming refresh and docs-facing real-data asset verification are reserved for `workflow_dispatch`, capped with `timeout-minutes: 10`, and paired with the script-level `--max-runtime-s 480` guard to avoid long cancellation-prone runs.

Run a small-area pilot and publish docs-facing assets:

```bash
python scripts/run_streaming_wui_scaling.py \
  --bbox "-105.292,40.004,-105.236,40.047" \
  --outdir outputs/real_data_demo \
  --adj-buffer 250 \
  --epsilons "5,10,20,30,60,120" \
  --resolutions "30,60,90,120,150" \
  --veg-classes "41,42,43,52" \
  --network-timeout-s 45 \
  --max-network-attempts 1 \
  --max-runtime-s 480 \
  --publish-doc-assets
```

Primary run outputs are written under `outputs/real_data_demo/`:

```text
fixed_boundary_scaling.csv
fixed_boundary_scaling.png
resolution_rebuild_scaling.csv
resolution_rebuild_scaling.png
run_summary.json
```

When `--publish-doc-assets` is supplied, the script refreshes docs-facing publication assets:

```text
docs/assets/figures/real_fixed_boundary_scaling.png
docs/assets/figures/real_resolution_rebuild_scaling.png
docs/assets/data/real_fixed_boundary_scaling.csv
docs/assets/data/real_resolution_rebuild_scaling.csv
```

CI and local pre-PR site review now include an explicit hard check for these four docs-facing real-data assets. If any are missing, the workflow exits with a clear error instead of allowing a successful docs build with implied-but-absent empirical outputs.

The local analysis run refreshes the published synthetic assets used by the manuscript pages:

```text
docs/assets/figures/boundary_scaling_plot.svg
docs/assets/figures/satellite_resolution_scaling_plot.svg
docs/assets/data/boundary_scaling_summary.csv
docs/assets/data/satellite_resolution_scaling_summary.csv
```

For exploratory sweeps that should not overwrite website assets, use `--skip-doc-publish`:

```bash
python scripts/run_minimal_boundary_scaling.py \
  --output-subdir epsilon_dense \
  --min-epsilon 1 \
  --max-epsilon 40 \
  --n-steps 20 \
  --vegetation-threshold 0.45 \
  --neighborhood-radius-m 200 \
  --adjacency-rule intersects \
  --skip-doc-publish \
  --include-satellite-demo
```

Additional CLI options are available through:

```bash
python scripts/run_minimal_boundary_scaling.py --help
python scripts/run_streaming_wui_scaling.py --help
```

In pull requests, generated artifacts are attached for review in CI. Publication to GitHub Pages still occurs through the repository’s manual dispatch release workflow when maintainers decide to promote a validated revision.

Playwright-backed local review remains part of the expected validation path for website-facing changes, and `scripts/pre_pr_site_review.sh` is the canonical entry point for that check. If geospatial runtime support or network access is unavailable, the streaming pilot may fail before publication; in that case, do not publish placeholders—fix the environment or fail the check clearly.

For prompt-level reconstruction of the workflow narrative and implementation sequence, see [Reproducible prompts](reproducible-prompts.md). For the synthetic-to-empirical handoff now scaffolded in code, see [Real-data experiments](real-data-experiments.md). The staged development context for both is summarized in the [Project roadmap](project-roadmap.md).

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
- `scripts/run_minimal_boundary_scaling.py` — reproducible synthetic run with CLI flags.
- `tests/test_scaffold.py` — minimal behavior checks.
- `outputs/minimal_demo/` — run outputs and summaries.
- `docs/assets/data/` and `docs/assets/figures/` — published docs-facing artifacts.

## When results are generated

### Local execution

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_minimal_boundary_scaling.py
```

By default, this local command writes to both:

- raw/local outputs: `outputs/minimal_demo/`
- website-facing assets: `docs/assets/figures/` and `docs/assets/data/`

### GitHub Actions execution

The workflow `.github/workflows/boundary-scaling-demo.yml` triggers on:

- `pull_request`
- `workflow_dispatch` (manual run)

On both triggers, CI runs tests + the synthetic demo, and uploads `outputs/minimal_demo/` as an artifact.

## How site outputs get updated

Important distinction:

- **Workflow artifacts** are temporary run outputs you download from Actions.
- **Website-published assets** are committed files in `docs/assets/`.

In this repo, docs assets are only committed back to the branch when:

- event is `workflow_dispatch`, and
- actor is not `github-actions[bot]`.

So PR runs validate and generate artifacts, but do not refresh the published site unless someone manually dispatches the workflow (or commits local docs asset updates).

## How to test changes

### 1) Standard local run (default scenario)

```bash
python scripts/run_minimal_boundary_scaling.py
```

Inspect:

- `outputs/minimal_demo/run_summary.md`
- `outputs/minimal_demo/boundary_scaling_summary.csv`
- `outputs/minimal_demo/boundary_scaling_plot.png`
- `docs/assets/data/boundary_scaling_summary.csv`
- `docs/assets/figures/boundary_scaling_plot.svg`

### 2) Local parameter sweep / alternate scenario

The demo script now supports lightweight CLI parameters:

```bash
python scripts/run_minimal_boundary_scaling.py \
  --output-subdir epsilon_dense \
  --min-epsilon 1 \
  --max-epsilon 40 \
  --n-steps 20 \
  --vegetation-threshold 0.45 \
  --neighborhood-radius-m 200 \
  --adjacency-rule intersects \
  --skip-doc-publish
```

Use `--skip-doc-publish` for experiments you do not want copied into `docs/assets/`.

### 3) Pull request validation path

- Open/update a PR.
- Confirm `Boundary Scaling Demo` workflow succeeds.
- Download `boundary-scaling-minimal-demo` artifact to inspect run outputs.

### 4) Manual GitHub Actions publish path

- Run `Boundary Scaling Demo` via **Run workflow** in Actions (`workflow_dispatch`).
- The `publish-doc-assets` job copies artifact outputs into `docs/assets/*` and commits changes back when files changed.
- Verify the commit appears on the branch that backs GitHub Pages.

## CLI options reference

`python scripts/run_minimal_boundary_scaling.py --help`

Supported flags:

- `--output-subdir` (default `minimal_demo`)
- `--min-epsilon` (default `1.0`)
- `--max-epsilon` (default `30.0`)
- `--n-steps` (default `8`)
- `--vegetation-threshold` (default `0.35`)
- `--neighborhood-radius-m` (default `120.0`)
- `--adjacency-rule` (default `touches`)
- `--skip-doc-publish` (default disabled)


## Deployed website QA review (Playwright)

In addition to the synthetic analysis workflow, this repository now includes browser-based QA for the published GitHub Pages site itself:

- workflow: `.github/workflows/playwright-site-review.yml`
- trigger: `pull_request` and manual `workflow_dispatch`
- target URL: `https://cu-esiil.github.io/WUI_boundary/` (deployed site, not localhost)

The review checks:

- basic page health (navigation, title, `main` content, no obvious 404 text),
- homepage narrative + key links,
- interactive iframe visibility and fallback full-page link,
- scaling-results figure load state, CSV link, and rendered table rows,
- console/page errors and failed network requests (attached as diagnostics).

Run artifacts include `playwright-report` and `playwright-test-results` (screenshots for key pages plus traces/videos on failures).

## Forward path to empirical analysis

The next step is not a redesign of the conceptual claim; it is empirical activation of the same \(L_d(\varepsilon)\) framework with transparent data provenance, reproducible preprocessing, and explicit uncertainty reporting.

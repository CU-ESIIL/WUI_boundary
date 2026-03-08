# Methods & reproducibility

The current analytical pipeline is a deliberately simplified scaffold for testing the logic of \(L_d(\varepsilon)\) before empirical WUI datasets are brought fully into the workflow. Rather than treating synthetic output as a substitute for real landscape analysis, the pipeline uses toy geometry to make the structure of the problem explicit and reproducible.

This matters because the core claim of the project is methodological as much as geometric. Boundary length must be interpreted in relation to how the boundary object was defined and how the measurement scale was chosen. A small, transparent, synthetic pipeline is therefore useful not because it resolves the empirical question, but because it demonstrates the analytical wiring needed to ask that question clearly.

What follows documents the current execution pathway, the published outputs, and the local and continuous-integration routes through which figures and summary data are regenerated. The purpose of this page is practical, but it should be read in continuity with the rest of the site: reproducibility here serves interpretation, not just software maintenance.

Install dependencies and run baseline checks:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/run_minimal_boundary_scaling.py --include-satellite-demo
```

Run the website validation gate for docs and UI-facing changes:

```bash
scripts/pre_pr_site_review.sh
```

The local analysis run refreshes the published assets used by the manuscript pages:

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
```

In pull requests, generated artifacts are attached for review in CI. Publication to GitHub Pages still occurs through the repository’s manual dispatch release workflow when maintainers decide to promote a validated revision.

Playwright-backed local review remains part of the expected validation path for website-facing changes, and `scripts/pre_pr_site_review.sh` is the canonical entry point for that check.

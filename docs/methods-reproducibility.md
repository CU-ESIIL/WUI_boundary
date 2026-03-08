# Methods & reproducibility

The current analytical pipeline is intentionally designed as a synthetic scaffold for studying the logic of \(L_d(\varepsilon)\) before full empirical ingestion. It lets the project test assumptions about delineation and measurement scale in a transparent environment where every transformation is inspectable and reproducible.

This scaffold should be read as a methods prototype rather than a claim about final empirical WUI magnitudes. The synthetic boundary objects and scale sweeps are used to validate reasoning, figure generation, and reporting structure so that later real-data analyses can be interpreted within the same framework.

Reproducibility is therefore treated as part of the scientific argument. The same commands used for local checks generate the docs-facing CSV and figure outputs, and the same checks are exercised in automated review.

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

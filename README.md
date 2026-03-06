# WUI_boundary

This repository contains the `WUI_boundary` project website and analytics scaffold for scale-conditioned wildland-urban interface boundary length estimation.

It includes:

* project documentation and website content under `docs/` (MkDocs + Material)
* a UI draft section with a synthetic Story Lab prototype
* a lightweight Python analytics scaffold under `src/boundary_analytics`
* runnable synthetic demo scripts and outputs for reproducible workflow wiring
* project history and governance files such as `CHANGELOG.md` and `AGENTS.md`

The website is built from the `docs/` folder and deployed with GitHub Pages.

---

# Website deployment

Enable GitHub Pages with **Source: GitHub Actions** in repository settings.

Expected site URL:

```
https://cu-esiil.github.io/WUI_boundary/
```

---

# Preview locally

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open:

```
http://127.0.0.1:8000
```

---

## Current milestone: executable minimal boundary scaling demo

This repository currently includes:

- a **UI Drafts** docs section with a presentation-ready synthetic Draft 1 Story Lab
- a **Roadmap to Real Data** page describing the next analytic steps
- a lightweight Python **boundary analytics scaffold** under `src/boundary_analytics`
- an executable synthetic analysis runner at `scripts/run_minimal_boundary_scaling.py`

These additions are intentionally scaffold-level and do not claim completed real-data analytics.

## Re-run the current minimal analysis milestone

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run tests:

```bash
python -m unittest discover -s tests -v
```

3. Run the minimal synthetic boundary-scaling analysis:

```bash
python scripts/run_minimal_boundary_scaling.py
```

4. Inspect outputs in:

- `outputs/minimal_demo/boundary_scaling_summary.csv`
- `outputs/minimal_demo/run_summary.md`

The generated outputs are **synthetic** and only demonstrate executable plumbing for
\(L_d(\varepsilon)\), where `d` is delineation choice and `epsilon` is measurement scale.

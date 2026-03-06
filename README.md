# Research Project Template

This repository is a **minimal template for research and data science projects** that combine code, documentation, and a project website.

It includes:

* a clean project structure (`src`, `data`, `docs`, `tests`, etc.)
* a documentation website built with **MkDocs + Material**
* automatic deployment to **GitHub Pages** using GitHub Actions
* development history files (changelog, roadmap, dev log)
* an `AGENTS.md` file with guidance for AI coding agents

The website is built from the `docs/` folder and automatically deployed when changes are pushed.

---

# Enable the Website

After creating a repository from this template you must enable GitHub Pages once.

1. Go to **Settings → Pages**
2. Under **Build and deployment**, choose
   **Source: GitHub Actions**

The site will then deploy automatically on push.

Your site will appear at:

```
https://<your-username>.github.io/<repository-name>/
```

---

# Preview Locally

```
pip install -r requirements.txt
mkdocs serve
```

Then open:

```
http://127.0.0.1:8000
```

---

## Current Milestone: Executable Minimal Boundary Scaling Demo

This repository now includes:

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

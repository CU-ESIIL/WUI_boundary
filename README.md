# WUI Boundary Scaling

How long is the Wildland–Urban Interface boundary? At first glance, this sounds like a straightforward measurement problem: draw the line separating developed places from wildland vegetation and compute its length. But that apparent simplicity collapses as soon as method enters the picture. The measured boundary depends on what we decide counts as the boundary in the first place, and on the scale at which we measure it.

This repository is organized around that scientific problem. It treats WUI boundary length not as a single fixed quantity to be reported once, but as a value conditioned by assumptions and resolution. The project combines narrative scientific interpretation, interactive web-based exploration, and a compact analytics workflow so that the conceptual argument and the computational logic remain tied together.

## The idea

The intuition is familiar from the coastline paradox: as measurement becomes finer, irregular boundaries often appear longer. The WUI boundary can behave similarly. A coarser ruler smooths local complexity and yields a shorter estimate; a finer ruler resolves more structure and yields a longer one.

A second source of variation is delineation. Changing the definition of what counts as "WUI boundary" changes the object being measured, not just the instrument used to measure it. In other words, there are two different levers: one changes the boundary itself, and the other changes the scale of measurement applied to that boundary.

In this project, measured boundary length is written as \(L_d(\epsilon)\), where \(d\) denotes delineation choice (the boundary definition) and \(\epsilon\) denotes measurement scale (effective ruler length or resolution). The central claim is that WUI boundary length should be treated as a scale-conditioned quantity, not a fixed scalar.

## What this repository contains

This repository contains a scientific website in `docs/` that presents the argument as a narrative investigation rather than as a static reference page. It also includes interactive prototypes in `docs/ui-drafts/` that help communicate scale dependence and definition dependence in a more exploratory format. Alongside those materials is a small analytics framework in `src/boundary_analytics/` and executable scripts in `scripts/` that demonstrate the scaling logic with synthetic geometries.

The current code-and-docs pairing is intentionally explicit: the website explains the reasoning, and the scripts show how \(L_d(\epsilon)\) can be produced in practice. Outputs from demo runs are written to `outputs/` and selected artifacts are mirrored into `docs/assets/` for web presentation.

## Repository structure

The core layout is compact. `docs/` contains the website narrative, while `docs/ui-drafts/` holds interactive draft experiments. `src/wui_boundary/` is not used in this repository; the analytics code currently lives in `src/boundary_analytics/`. `scripts/` contains runnable analysis entry points. `outputs/` stores generated demo artifacts. `tests/` includes lightweight checks for the analytics scaffold. Site configuration lives in `mkdocs.yml`.

## Running the demo analysis

```bash
python -m pip install -e .
python scripts/run_minimal_demo.py
```

Demo outputs are written to `outputs/` (specifically `outputs/minimal_demo/` for the current minimal run). The canonical runtime install path is editable package install (`python -m pip install -e .`), which includes geospatial dependencies for the streaming real-data pilot. `requirements.txt` is reserved for documentation tooling (MkDocs) layered on top when needed.


## Automated deployed-site review (Playwright)

The repository includes a lightweight Playwright reviewer that checks the deployed GitHub Pages site at:

- `https://cu-esiil.github.io/WUI_boundary/`

It runs on pull requests and can also be launched manually from the Actions tab using the **Playwright Site Review** workflow. The review focuses on key scientific pages and catches common publication failures (broken page loads, missing figure/table/iframe content, console errors, and obvious navigation regressions).

Artifacts from each run are available in GitHub Actions:

- `playwright-report` (HTML report)
- `playwright-test-results` (screenshots, traces on failure, and JSON diagnostics for console/request issues)

You can also run it locally:

```bash
npm install
npx playwright install --with-deps chromium
npm run test:site-review
```

## Local pre-PR website review (Codex and contributors)

Run this before opening or proposing a PR for website-related changes:

```bash
npm run review:site
```

This one command runs the site-facing analysis step (`python scripts/run_minimal_demo.py`), performs `mkdocs build --strict`, ensures Playwright dependencies are installed, and executes local Playwright tests.

If Playwright fails, inspect artifacts and fix before retrying:

- `playwright-report/` for the HTML report
- `test-results/` for screenshots, traces, and videos on failure

GitHub Actions remains the final CI gate, but local review should catch most website/UI regressions earlier.

## Project status

At present, the repository demonstrates the conceptual framework with synthetic boundary geometries and synthetic scaling outputs. It is designed to grow toward empirical WUI datasets and case-based analyses while keeping delineation choices, measurement scale, and interpretation transparent.

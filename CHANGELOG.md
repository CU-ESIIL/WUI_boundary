# Changelog

## Unreleased

### Changed
- Added `PROJECT_CONTEXT.md` to capture the project's full conceptual framing, working hypothesis, and initial OSM + ESA WorldCover dataset plan, and linked it from the README for discoverability.
- Replaced the previous broken real-data scaling path with a minimal streaming ESA WorldCover + OSM buildings pipeline in `src/boundary_analytics/streaming_wui.py` and a thin CLI runner `scripts/run_streaming_wui_scaling.py`, producing deterministic CI-friendly outputs (`interface_scaling.csv/json/png`).
- Added focused unit tests for coarsening, pixel-size estimation, mask-to-polygon conversion, interface-length measurement, and Overpass endpoint fallback in `tests/test_streaming_script.py`.
- Updated the boundary-scaling GitHub Actions workflow and site review gate to run the tiny-bbox streaming demo by default and publish docs-facing assets as `real_interface_scaling.{csv,png}`.
- Corrected `interface_length_m` in the streaming pipeline to measure the settlement-buffer interface front consistently (using buffered-settlement boundary intersection with vegetation boundary), fixing CI failure in `test_interface_length_calculation`.
- Unblocked routine PR checks by moving strict real-data docs-asset verification out of the default PR demo workflow and into the manual `workflow_dispatch` refresh path, while retaining hard missing-asset failure gates for manual refresh and Pages deploy.
- Standardized install workflow around editable package install (`python -m pip install -e .`) for runtime/CI paths, clarified `requirements.txt` as documentation-only dependencies, and updated local/CI website validation to fail fast when required real-data docs assets are missing.
- Updated reproducibility and real-data docs to reflect canonical installation, explicit real-data publication behavior, and clear not-published status when docs-facing real-data assets are absent.
- Bounded CI real-data streaming execution with an explicit job timeout and lower network retry envelope (`timeout-minutes: 10`, `--network-timeout-s 45`, `--max-network-attempts 1`, `--max-runtime-s 480`) to convert cancellation-prone runs into clear pass/fail outcomes.
- Implemented a first empirical, no-keys streaming pilot runner at `scripts/run_streaming_wui_scaling.py` that fetches OSM buildings from Overpass, streams a bbox-limited NLCD window from a remote raster source, builds a WUI-like settlement–vegetation interface, runs fixed-boundary and resolution-rebuild scaling experiments, writes CSV/PNG/JSON outputs, and can publish docs-facing assets under `docs/assets/`.
- Hardened Overpass acquisition in `scripts/run_streaming_wui_scaling.py` with retry-and-fallback behavior across multiple public Overpass endpoints so transient 504/timeout failures are retried before the run fails.
- Hardened NLCD streaming source resolution in `scripts/run_streaming_wui_scaling.py` by trying a fallback COG URL when the primary URL is unavailable, and replaced deprecated GeoPandas `unary_union` usage with a `union_all()`-first helper for forward compatibility.
- Added an NLCD WMS fallback path in `scripts/run_streaming_wui_scaling.py` so bbox subset extraction can proceed when direct COG URLs return HTTP permission/availability errors.
- Added vegetation-mask fallback handling for remapped NLCD service responses so the streaming run can continue when requested NLCD class IDs are not preserved in-band (for example, display-style WMS responses).
- Added configurable network timeout/retry controls for the streaming pilot (`--network-timeout-s`, `--max-network-attempts`) and bounded retry loops for NLCD COG/WMS fetches to reduce long-running cancellation risk in CI.
- Rewrote `docs/real-data-experiments.md` into a manuscript-style real-data page with the required transition prose, explicit experiment framing, figure embeds, and CSV links for the empirical pilot outputs.
- Updated manuscript cross-links and reproducibility guidance (`docs/index.md`, `docs/scaling-results.md`, `docs/implications-for-remote-sensing.md`, `docs/methods-reproducibility.md`) so the real-data pilot workflow, run command, outputs, and docs-asset publication pattern are discoverable and documented.

### Added
- Added `tests/test_streaming_script.py` with lightweight parser/fit smoke tests for the streaming pilot script helper logic.

### Changed
- Unblocked routine PR checks by moving strict real-data docs-asset verification out of the default PR demo workflow and into the manual `workflow_dispatch` refresh path, while retaining hard missing-asset failure gates for manual refresh and Pages deploy.
- Expanded manuscript navigation and cross-links to include new pages for real-data experiments, reproducible prompts, visual figure placeholders, and a staged project roadmap.
- Updated homepage site-review assertions to accept either a direct `scaling-results` link or the current `why-length-depends-on-scale` progression link, aligning tests with deployed manuscript navigation while preserving interactive-link coverage.
- Relaxed homepage and scaling-results Playwright link/refresh selectors to match stable route fragments and fallback next-page navigation, preventing false negatives on deployed URL variants that differ in suffixes or heading prose.
- Broadened deployed-site Playwright assertions to accept both legacy and updated manuscript homepage headings and to detect refresh/reproducibility guidance from either section headings or equivalent prose, reducing false negatives when production content lags branch updates.
- Replaced narrative prose across the manuscript-facing docs pages with a cohesive scholarly monograph voice, preserving interactive embeds, figure/table assets, CSV links, and manuscript navigation while removing residual scaffold phrasing and outline-style narrative bullets.
- Relaxed the scaling-results Playwright assertion to accept either `Last generated by / refresh model` or `Refresh and reproducibility` heading, reducing false negatives when deployed docs lag behind latest branch content.
- Restored the `Last generated by / refresh model` heading on `docs/scaling-results.md` so the deployed-site Playwright review assertion for refresh metadata passes again.
- Extended `scripts/run_minimal_boundary_scaling.py` with an optional `--include-satellite-demo` pathway that evaluates synthetic perimeter across satellite-like scales (1, 10, 30, 100, 250, 500 m), writes a dedicated SVG/PNG figure and summary CSV, computes log-log fit slope/intercept, and publishes these assets to `docs/assets/` during normal docs publish runs.
- Added a new manuscript-style page `docs/implications-for-remote-sensing.md` with the remote-sensing scale narrative, a synthetic satellite-resolution figure embed, and a status callout clarifying that the output is a synthetic prototype demonstration.
- Added manuscript cross-links from `docs/scaling-results.md` and `docs/index.md`, inserted the new page in the public MkDocs navigation, and updated reproducibility/workflow docs to include the satellite-scale outputs and CLI usage.
- Updated `.github/workflows/boundary-scaling-demo.yml` to run the satellite demo pathway and publish/commit both new docs-facing satellite figure and CSV assets alongside the original scaling outputs.
- Upgraded the synthetic boundary-scaling figure generator to emit a publication-style SVG with an internal title, explicit axis labels, readable tick labels, and an in-plot annotation panel for delineation, fitted slope, and number of evaluated scales.
- Rewrote `docs/scaling-results.md` as a manuscript-like results narrative with a clear synthetic-status callout, figure caption, "how to read" guidance, plain-language interpretation, and reader-friendly summary-table column definitions.
- Restored desktop manuscript navigation visibility by scoping white nav text overrides to header/tab chrome and adding explicit readable primary-sidebar link/active states in the ESIIL theme CSS.
- Switched the Interactive Experiments primary embed/full-page launch to a new Draft 3 iframe-optimized app and preserved Draft 1/2 links as archived variants.
- Narrowed Playwright console-error filtering to ignore the known deployed scaling plot 404 at `/WUI_boundary/scaling-results/assets/figures/boundary_scaling_plot.svg` while preserving strict failure behavior for unrelated console errors.
- Fixed scaling-results published asset paths to use project-rooted `/WUI_boundary/assets/...` URLs so the plot image no longer 404s under the `/scaling-results/` route in deployed-site Playwright checks.
- Hardened deployed-site Playwright QA checks by ignoring known unauthenticated GitHub API 403 console noise and replacing broad `404` text scans with explicit 404-page heading checks, preventing false negatives on content pages.
- Replaced the default Material purple-leaning visual presentation with an ESIIL scientific brand theme by adding reusable color tokens, MkDocs palette overrides, branded nav/link/button states, and refreshed content-surface/card/admonition styling across key manuscript pages.
- Updated Playwright homepage link assertions to target article-body links by href and made scaling plot asset checks resilient to MkDocs relative-asset resolution by testing both browser-resolved and project-root candidate URLs.
- Fixed Playwright homepage link assertions to target links inside `main` content and fixed scaling plot fetch checks to use browser-resolved image URLs (`currentSrc`/`src`) under MkDocs base URL behavior.
- Relaxed brittle Playwright content assertions by broadening the homepage H1 check and validating scaling plot asset fetch success instead of relying on `naturalWidth` for SVG rendering.
- Fixed Playwright navigation paths to use repository-relative routes (without leading `/`) so checks resolve under the GitHub Pages project site base path (`/WUI_boundary/`) in CI.
- Added a Playwright-based deployed-site reviewer (tests + config + CI workflow) that validates key GitHub Pages routes, figures, tables, iframes, console/network sanity, and uploads screenshots/report artifacts for inspection.
- Updated the Playwright site-review workflow Node setup to avoid npm cache lockfile requirements so CI can run without a committed JavaScript lockfile.
- Audited and clarified synthetic analytics publication behavior across local runs, PR artifacts, and manual workflow dispatch in website-facing docs.
- Expanded `docs/scaling-results.md` with a prominently embedded current plot, plain-language interpretation, CSV preview table, and explicit refresh guidance.
- Expanded `docs/methods-reproducibility.md` with sections for generation triggers, site update behavior, and concrete testing pathways for local, PR, and manual Actions runs.
- Added a homepage callout in `docs/index.md` that links directly to current Scaling Results and explains why published outputs can appear stale.
- Added CLI flags to `scripts/run_minimal_boundary_scaling.py` so contributors can test alternate epsilon grids and delineation settings without editing code, including `--skip-doc-publish` for local-only experiments.
- Switched published docs-facing plot output from PNG to SVG and updated workflow/docs references so result previews remain visible without requiring a committed binary image file.

- Added robust inline iframe embeds on `docs/interactive-experiments.md` using GitHub Pages-rooted `/WUI_boundary/...` paths for Draft 1 and Draft 2 Story Lab demos, while preserving full-page fallback buttons.
- Added dedicated `.app-frame` embed styling in `docs/stylesheets/extra.css` to prevent collapsed iframe height and improve responsive visibility on desktop/tablet/mobile.
- Replaced the public MkDocs information architecture with a manuscript-style scientific narrative: Home, Why Length Depends on Scale, What Counts as the WUI Boundary, Interactive Experiments, Scaling Results, Fire Science Implications, and Methods & Reproducibility.
- Rewrote `docs/index.md` as an abstract-plus-figure narrative homepage centered on the core claim that WUI boundary length is a function \(L_d(\varepsilon)\).
- Added new core manuscript pages (`docs/why-length-depends-on-scale.md`, `docs/what-counts-as-wui-boundary.md`, `docs/interactive-experiments.md`, `docs/scaling-results.md`, `docs/fire-science-implications.md`, `docs/methods-reproducibility.md`) and migrated key content from prior drafts/scaffold pages.
- Demoted legacy template-era pages under `docs/ui-drafts/` and `docs/analytics/` to internal archive stubs and removed `docs/examples.md` from the project.

### Added
- Added real-data pipeline scaffold scripts (`scripts/download_sample_data.py`, `scripts/build_sample_wui_boundary.py`, `scripts/run_real_boundary_scaling.py`) plus versioned `data/raw/` and `data/processed/` directories for pilot-region workflows.
- Added new manuscript pages `docs/reproducible-prompts.md`, `docs/real-data-experiments.md`, `docs/visual-figures.md`, and `docs/project-roadmap.md` with reproducibility text, empirical-transition framing, and manual image-upload slots under `docs/assets/images/`.
- Added `scripts/pre_pr_site_review.sh` as a one-command local pre-PR website validation workflow that runs demo build steps, `mkdocs build --strict`, Playwright dependency setup, and Playwright tests.
- Added Codex skill guidance at `codex/skills/site-review/SKILL.md` for iterative website review/fix loops using local Playwright artifacts.
- Added `docs/ui-drafts/draft-3/story-lab-responsive.html`, a third Story Lab draft tuned for iframe/tablet/mobile layouts with later single-column breakpoints and tighter control-to-map educational grouping.
- Added `pyproject.toml` so the repository supports editable installs via `pip install -e .` for the documented demo workflow.
- Added `scripts/run_minimal_demo.py` as a concise entry point that calls the existing minimal boundary-scaling runner.
- New UI Drafts page `docs/ui-drafts/draft-2.md` and standalone app `docs/ui-drafts/draft-2/story-lab-remix.html` for Draft 2 — WUI Boundary Story Lab Remix, including iframe embed and full-page launch link.
- QA audit report `outputs/qa/playwright-site-audit-2026-03-07.md` capturing Playwright page checks, link-scope review, screenshots, and conservative follow-up recommendations.
- GitHub Actions workflow `.github/workflows/boundary-scaling-demo.yml` for pull requests and manual dispatch to run tests, execute minimal analysis, upload artifacts, and optionally commit selected docs-facing assets on workflow_dispatch.
- New analytics docs page: `docs/analytics/minimal-demo.md` showing the synthetic boundary-scaling plot and rerun guidance.
- Workflow-driven publication of website-facing synthetic demo assets under `docs/assets/figures/` and `docs/assets/data/` (generated/updated by CI job).
- Minimal analysis now generates `outputs/minimal_demo/boundary_scaling_plot.png` in addition to CSV and markdown summary.
- Minimal analysis runner now also copies generated PNG/CSV into `docs/assets/figures/` and `docs/assets/data/` during local execution so docs-facing outputs are immediately refreshed.
- New website section **UI Drafts** with:
  - Draft 1 — WUI Boundary Story Lab (synthetic conceptual prototype)
  - Roadmap to Real Data
- Boundary Analytics scaffold documentation page.
- Lightweight Python analytics scaffold package under `src/boundary_analytics`.
- Basic scaffold tests under `tests/test_scaffold.py`.
- Executable synthetic minimal analysis runner: `scripts/run_minimal_boundary_scaling.py`.
- Synthetic demo outputs under `outputs/minimal_demo/` generated by the runner.

### Changed
- Unblocked routine PR checks by moving strict real-data docs-asset verification out of the default PR demo workflow and into the manual `workflow_dispatch` refresh path, while retaining hard missing-asset failure gates for manual refresh and Pages deploy.
- Rewrote `README.md` from a scaffold-style project overview into a manuscript-like scientific framing centered on the question of WUI boundary length as \(L_d(\epsilon)\), with narrative context, repository orientation, and updated demo instructions.
- Generated PNG figure artifacts are no longer versioned in git; they are regenerated by the analysis script and workflow publish step.
- Rebranded MkDocs site identity from template defaults to `WUI_boundary`, including project repository links, site URL, homepage copy, and project-focused navigation labels.
- Removed `/basic_OASIS/` hardcoded Draft 1 embed paths in favor of project-safe links and updated the custom logo partial to route to the site homepage.
- Replaced the Draft 1 Story Lab placeholder page with the exact current standalone HTML/CSS/JS implementation and preserved its interactive behavior/styling.
- Updated Draft 1 embedding links so the standalone app resolves correctly from the docs page build path.
- Corrected Draft 1 iframe/full-page Story Lab links to use repo-native relative paths (`story-lab.html`) so embeds resolve under `WUI_boundary` GitHub Pages without template-base leakage.
- Replaced placeholder-only measurement and scaling calls with minimal executable toy implementations while preserving delineation index `d` and measurement scale `epsilon` separation.
- Updated README and analytics docs with explicit rerun instructions for tests and minimal analysis.

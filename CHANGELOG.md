# Changelog

## Unreleased

### Changed
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
- Rewrote `README.md` from a scaffold-style project overview into a manuscript-like scientific framing centered on the question of WUI boundary length as \(L_d(\epsilon)\), with narrative context, repository orientation, and updated demo instructions.
- Generated PNG figure artifacts are no longer versioned in git; they are regenerated by the analysis script and workflow publish step.
- Rebranded MkDocs site identity from template defaults to `WUI_boundary`, including project repository links, site URL, homepage copy, and project-focused navigation labels.
- Removed `/basic_OASIS/` hardcoded Draft 1 embed paths in favor of project-safe links and updated the custom logo partial to route to the site homepage.
- Replaced the Draft 1 Story Lab placeholder page with the exact current standalone HTML/CSS/JS implementation and preserved its interactive behavior/styling.
- Updated Draft 1 embedding links so the standalone app resolves correctly from the docs page build path.
- Corrected Draft 1 iframe/full-page Story Lab links to use repo-native relative paths (`story-lab.html`) so embeds resolve under `WUI_boundary` GitHub Pages without template-base leakage.
- Replaced placeholder-only measurement and scaling calls with minimal executable toy implementations while preserving delineation index `d` and measurement scale `epsilon` separation.
- Updated README and analytics docs with explicit rerun instructions for tests and minimal analysis.

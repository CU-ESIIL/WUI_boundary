# Playwright QA Audit — 2026-03-07

Audited target site: `https://cu-esiil.github.io/WUI_boundary/`

## Scope

- Home page
- UI Draft 1 page
- Story Lab full-page app
- Roadmap page
- Analytics pages:
  - Boundary Analytics Scaffold
  - Minimal Demo Output

## Summary

All audited pages returned HTTP 200 and rendered non-empty content. No links pointing to `basic_OASIS` or obvious template path URLs were found in visible links on audited pages.

The Draft 1 page includes a Story Lab iframe and a full-page Story Lab link. Both targets resolve successfully.

## Page-by-page results

| Page | URL | HTTP | Visible 404 | Non-blank | Notes |
|---|---|---:|---|---|---|
| Home | `https://cu-esiil.github.io/WUI_boundary/` | 200 | No | Yes | Only expected off-site links (GitHub repo, MkDocs theme credit). |
| Draft 1 | `https://cu-esiil.github.io/WUI_boundary/ui-drafts/draft-1/` | 200 | No | Yes | Iframe present (`src="story-lab.html"`), full-page Story Lab link resolves. |
| Story Lab | `https://cu-esiil.github.io/WUI_boundary/ui-drafts/draft-1/story-lab.html` | 200 | No | Yes | Key controls render (definition radius, measurement scale, roughness, housing pressure, narrative mode buttons). |
| Roadmap | `https://cu-esiil.github.io/WUI_boundary/ui-drafts/roadmap-to-real-data/` | 200 | No | Yes | Internal links stayed in repo/site scope. |
| Analytics Scaffold | `https://cu-esiil.github.io/WUI_boundary/analytics/scaffold/` | 200 | No | Yes | Internal links stayed in repo/site scope. |
| Minimal Demo Output | `https://cu-esiil.github.io/WUI_boundary/analytics/minimal-demo/` | 200 | No | Yes | Internal links stayed in repo/site scope. |

## Broken or suspicious URLs

No broken URLs detected in the audited pages.

No visible links to `basic_OASIS` or explicit template path URLs were detected.

Observed off-site links were expected project metadata or theme credit links:

- `https://github.com/CU-ESIIL/WUI_boundary`
- `https://squidfunk.github.io/mkdocs-material/`

## Recommended conservative follow-ups

1. Add an optional automated link/domain allowlist CI check for docs pages to ensure future links stay under the project site/repo unless explicitly approved.
2. Add a lightweight browser smoke test for key pages (`/`, Draft 1, Story Lab, roadmap, analytics pages) to catch regressions in routing or blank renders.
3. If desired, replace template-adjacent visual naming (e.g., `oasis-*` class names) with project-specific naming over time to reduce template-carryover ambiguity.

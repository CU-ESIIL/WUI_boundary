# Site Review Skill

Use this skill whenever a task changes website-facing behavior, including docs content, CSS/styling, MkDocs config, JavaScript, interactive HTML, iframe embeds, or published assets.

## Goal
Catch and fix website regressions locally before preparing a pull request.

## Required workflow
1. Run the one-command local pre-PR check:
   ```bash
   scripts/pre_pr_site_review.sh
   ```
2. If Playwright fails, inspect artifacts before editing:
   - `playwright-report/` (HTML report)
   - `test-results/` (failure screenshots, traces, videos, diagnostics)
3. Apply the smallest fix that resolves the failure.
4. Re-run `scripts/pre_pr_site_review.sh`.
5. Repeat until all checks pass.

## Definition of done for website tasks
- `scripts/pre_pr_site_review.sh` exits successfully.
- Playwright tests are passing locally.
- No PR should be prepared/proposed until those checks are green.

## Notes
- GitHub Actions Playwright checks remain the final CI gate.
- Local review is required to catch UI regressions earlier and reduce late CI failures.

import { test, expect } from '@playwright/test';
import { attachDiagnostics, saveReviewScreenshot } from './utils';

test('interactive experiments page renders iframe and fallback links', async ({ page }, testInfo) => {
  const diagnostics = attachDiagnostics(page, testInfo);

  const response = await page.goto('interactive-experiments/', { waitUntil: 'domcontentloaded' });
  expect(response?.ok()).toBeTruthy();

  await expect(page.locator('h1')).toContainText(/Interactive experiments/i);

  const iframe = page.locator('main iframe').first();
  await expect(iframe).toBeVisible();

  const box = await iframe.boundingBox();
  expect(box, 'Iframe should have a bounding box').not.toBeNull();
  expect((box?.width ?? 0) > 300, 'Iframe width should be non-trivial').toBeTruthy();
  expect((box?.height ?? 0) > 200, 'Iframe height should be non-trivial').toBeTruthy();

  await expect(page.getByRole('link', { name: /Open interactive figure in full page/i })).toBeVisible();

  const src = await iframe.getAttribute('src');
  expect(src).toContain('/WUI_boundary/ui-drafts/');

  await saveReviewScreenshot(page, testInfo, 'interactive-experiments');
  await diagnostics.assertAndAttach();
});

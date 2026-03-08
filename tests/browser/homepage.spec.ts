import { test, expect } from '@playwright/test';
import { assertNo404Page, attachDiagnostics, saveReviewScreenshot } from './utils';

test('homepage loads and links to key analysis pages', async ({ page }, testInfo) => {
  const diagnostics = attachDiagnostics(page, testInfo);

  const response = await page.goto('', { waitUntil: 'domcontentloaded' });
  expect(response?.ok()).toBeTruthy();

  await expect(page).toHaveTitle(/\S+/);
  await expect(page.locator('main')).toBeVisible();
  await expect(page.locator('h1')).toContainText(
    /WUI boundary length|How long is the Wildland[–-]Urban Interface boundary\?/i,
  );
  const article = page.locator('main article');
  await expect(article.locator('a[href="scaling-results/"]').first()).toBeVisible();
  await expect(article.locator('a[href="interactive-experiments/"]').first()).toBeVisible();
  await assertNo404Page(page);

  await saveReviewScreenshot(page, testInfo, 'homepage');
  await diagnostics.assertAndAttach();
});

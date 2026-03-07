import { test, expect } from '@playwright/test';
import { attachDiagnostics, saveReviewScreenshot } from './utils';

test('homepage loads and links to key analysis pages', async ({ page }, testInfo) => {
  const diagnostics = attachDiagnostics(page, testInfo);

  const response = await page.goto('/', { waitUntil: 'domcontentloaded' });
  expect(response?.ok()).toBeTruthy();

  await expect(page).toHaveTitle(/\S+/);
  await expect(page.locator('main')).toBeVisible();
  await expect(page.locator('h1')).toContainText(/WUI boundary length/i);
  await expect(page.getByRole('link', { name: /Scaling Results/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /Interactive Experiments/i })).toBeVisible();
  await expect(page.getByText(/page not found|404/i)).toHaveCount(0);

  await saveReviewScreenshot(page, testInfo, 'homepage');
  await diagnostics.assertAndAttach();
});

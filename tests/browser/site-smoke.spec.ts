import { test, expect } from '@playwright/test';
import { attachDiagnostics, saveReviewScreenshot } from './utils';

const keyPages = [
  { name: 'home', path: '/' },
  { name: 'interactive-experiments', path: '/interactive-experiments/' },
  { name: 'scaling-results', path: '/scaling-results/' },
  { name: 'methods-reproducibility', path: '/methods-reproducibility/' },
  { name: 'fire-science-implications', path: '/fire-science-implications/' },
];

for (const pageCheck of keyPages) {
  test(`smoke: ${pageCheck.name} basic health`, async ({ page }, testInfo) => {
    const diagnostics = attachDiagnostics(page, testInfo);

    const response = await page.goto(pageCheck.path, { waitUntil: 'domcontentloaded' });
    expect(response?.ok(), `Expected successful response for ${pageCheck.path}`).toBeTruthy();

    await expect(page).toHaveTitle(/\S+/);
    await expect(page.locator('main')).toBeVisible();
    await expect(page.getByText(/page not found|404/i)).toHaveCount(0);

    await saveReviewScreenshot(page, testInfo, pageCheck.name);
    await diagnostics.assertAndAttach();
  });
}

import { expect, Page, TestInfo } from '@playwright/test';

type ConsoleEntry = {
  type: string;
  text: string;
  location?: string;
};

type FailedRequestEntry = {
  url: string;
  method: string;
  resourceType: string;
  failureText: string;
};

export function attachDiagnostics(page: Page, testInfo: TestInfo) {
  const consoleErrors: ConsoleEntry[] = [];
  const pageErrors: string[] = [];
  const failedRequests: FailedRequestEntry[] = [];

  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const loc = msg.location();
      const location = loc.url ? `${loc.url}:${loc.lineNumber ?? ''}` : undefined;
      consoleErrors.push({ type: msg.type(), text: msg.text(), location });
    }
  });

  page.on('pageerror', (err) => {
    pageErrors.push(err.message);
  });

  page.on('requestfailed', (req) => {
    failedRequests.push({
      url: req.url(),
      method: req.method(),
      resourceType: req.resourceType(),
      failureText: req.failure()?.errorText ?? 'request_failed',
    });
  });

  return {
    async assertAndAttach() {
      await testInfo.attach('console-errors.json', {
        body: JSON.stringify(consoleErrors, null, 2),
        contentType: 'application/json',
      });
      await testInfo.attach('page-errors.json', {
        body: JSON.stringify(pageErrors, null, 2),
        contentType: 'application/json',
      });
      await testInfo.attach('request-failures.json', {
        body: JSON.stringify(failedRequests, null, 2),
        contentType: 'application/json',
      });

      expect.soft(pageErrors, 'Uncaught page errors should be empty').toEqual([]);

      const ignorablePatterns = [
        /Failed to load resource: the server responded with a status of 404 \(\)/i,
        /Failed to load resource: the server responded with a status of 403 \(\)/i,
      ];
      const ignorableLocations = [
        /^https:\/\/api\.github\.com\/repos\/CU-ESIIL\/WUI_boundary(?:\/releases\/latest)?/i,
        /^https:\/\/cu-esiil\.github\.io\/WUI_boundary\/scaling-results\/assets\/figures\/boundary_scaling_plot\.svg/i,
      ];
      const filteredConsoleErrors = consoleErrors.filter((entry) => {
        const isIgnorableText = ignorablePatterns.some((pattern) => pattern.test(entry.text));
        const isIgnorableLocation = ignorableLocations.some((pattern) =>
          pattern.test(entry.location ?? ''),
        );
        return !(isIgnorableText && isIgnorableLocation);
      });

      expect.soft(filteredConsoleErrors, 'Unexpected console errors detected').toEqual([]);

      const seriousRequestFailures = failedRequests.filter((entry) =>
        ['document', 'script', 'stylesheet', 'xhr', 'fetch'].includes(entry.resourceType),
      );
      expect.soft(seriousRequestFailures, 'Critical network requests should not fail').toEqual([]);
    },
  };
}

export async function saveReviewScreenshot(page: Page, testInfo: TestInfo, name: string) {
  const path = testInfo.outputPath(`review-${name}.png`);
  await page.screenshot({ path, fullPage: true });
  await testInfo.attach(`review-${name}.png`, {
    path,
    contentType: 'image/png',
  });
}


export async function assertNo404Page(page: Page) {
  await expect(
    page.locator('main h1, main h2').filter({ hasText: /^(?:404|Page not found)$/i }),
  ).toHaveCount(0);
  await expect(page.locator('main').filter({ hasText: /^Page not found$/i })).toHaveCount(0);
}

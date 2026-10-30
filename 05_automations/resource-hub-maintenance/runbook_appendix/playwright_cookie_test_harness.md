# Playwright Cookie-Consent Test Harness

**Persona**: Site maintainer
**Purpose**: Reusable headless-Playwright snippet for testing `vanilla-cookieconsent` v3 banner DOM.
**Scope**: Use this harness when your resource hub includes a consent banner.
**Cross-references**: skillbook entries `browser-automation-tool-decision-001`, `cookie-consent-existing-wp-bridge-001`, `axe-truncation-unmasking-redirect-block-001`.

## The Problem

`vanilla-cookieconsent` v3 defaults to `hideFromBots: true`. In a typical Playwright Chromium context, `navigator.webdriver === true`. The library detects this and returns from `CookieConsent.run` without mounting the banner DOM:

```js
// Simplified representation of the v3 bot-detection check:
if (config.hideFromBots && (
  /bot|crawl|spider|slurp|teoma/i.test(navigator.userAgent) ||
  navigator.webdriver
)) return;
```

Result: Playwright tests find no banner and report no console errors. This can look like a broken banner even when it works for ordinary visitors.

## The Fix

Override `navigator.webdriver` in the test context BEFORE `page.goto`:

```js
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });

// Run before any page-level script. addInitScript injects pre-document.
await context.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
});

const page = await context.newPage();
await page.goto('https://example.com/resources/', { waitUntil: 'domcontentloaded' });

// Wait for the consent modal to mount.
await page.waitForSelector('#cc-main .cm', { timeout: 5000 });

const title = await page.locator('#cc-main .cm__title').textContent();
console.log('Banner title:', title);

await browser.close();
```

## What about cyclic axe scans?

Use the same override in a repeated axe scan, fix, and rescan workflow. Without it, axe scans a DOM missing the cookie banner, masking banner-related accessibility issues such as insufficient contrast. With it, the scan includes the banner that a first-time visitor would encounter.

## What NOT to do

- Do NOT set `hideFromBots: false` in the production `CookieConsent.run` configuration just to fix a test. That changes which automated visitors receive the banner. Apply the override only in the test context.
- Do NOT use Playwright MCP for this verification. Per `browser-automation-tool-decision-001`, use headless Node Playwright for repeatable verification and MCP-driven Playwright for interactive debugging. The `addInitScript` API works identically in both, but scripted checks are easier to repeat consistently.

## Special case: pages that auto-redirect

A kitchen-equipment maker's resource library might redirect from a download thank-you page to a spec sheet using a delayed `window.location.replace(assetUrl)` call and a meta-refresh fallback. Either can navigate away before axe finishes scanning. Block both in the test harness before navigation:

```js
await page.addInitScript(() => {
  // Intercept the redirect timer by inspecting its callback.
  // Directly overriding location.replace fails because it is non-configurable.
  const originalSetTimeout = window.setTimeout;
  window.setTimeout = function (fn, ms, ...args) {
    if (typeof fn === 'function' && fn.toString().includes('window.location.replace')) {
      return -1; // Suppress this redirect in the test context.
    }
    return originalSetTimeout.call(window, fn, ms, ...args);
  };

  // Remove the meta-refresh tag once the document has been parsed.
  document.addEventListener('readystatechange', () => {
    if (document.readyState !== 'loading') {
      document.querySelectorAll('meta[http-equiv="refresh" i]').forEach((m) => m.remove());
    }
  });
});
```

Match the timer interception to the page's actual redirect implementation. Callback inspection will miss other forms of navigation, and removing a meta-refresh tag after parsing assumes its delay allows time for removal.

Production redirects keep working. Only the test context blocks navigation so axe can scan the thank-you page. Verify the redirects separately without these overrides.

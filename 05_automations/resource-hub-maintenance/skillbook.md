# Resource Hub Maintenance: skillbook (generic edition)

> A strategy collection updated by the design-curator after every ACE iteration and after content operations reveal a reusable lesson. Entries explain the rule, its failure mode, and its reason so a person or small team can apply them to their own resource hub. Edition details: `05_automations/resource-hub-maintenance/EDITION_NOTES.md`.

> **Reading this edition**:
> - Use the Sanity HTTP API with your own token for content operations. See `05_automations/resource-hub-maintenance/runbook_appendix/sanity_content_ops.md`.
> - On **Vercel**, use preview branches and aliases as appropriate. On **Cloudflare Workers Builds**, use branch previews and configure the production branch explicitly. See `05_automations/resource-hub-maintenance/runbook_appendix/redeploy_cloudflare_workers.md`. Verify caching on the actual host before adopting a recipe from another platform.
> - Keep the site's content registry and Sanity records consistent.
> - Ground every product claim in the resource's own source document.
> - Connect forms, analytics, and review tools only when they are part of your site's configured stack.
> - Business examples are invented and illustrate reusable web-development lessons.
> - Rules include their reasons so they can be applied consistently.

**Version**: generic

---

## Content Skills (retained)

### content-003: Hybrid Page Strategy
In a hybrid routing setup, only resources with `htmlContent` get their own Astro page. PDFs link directly to the file. External resources link directly to their source page. This reduces the number of thin detail pages to maintain. Use it when a separate resource page would add no useful context; do not assume direct links provide the same indexing opportunities as substantive HTML pages.
- **Tags**: content, pages, seo, hybrid

### content-005: Rate Limiting for Sanity Operations
Use conservative starting limits: 100ms between document creates, 200ms after asset uploads, at most 10 parallel uploads, and at most 100 concurrent mutations. Retry HTTP 429 responses with exponential backoff of 2/4/8s, honoring `Retry-After` when supplied. Adjust concurrency to the project's actual limits and observed responses.
- **Tags**: content, rate-limiting, sanity

---

## Collection Skills (retained)

### collection-001: Product Hierarchy in Collections
Parent product collections aggregate all children through a scoped wildcard GROQ match. For an invented kitchen-equipment maker, a mixer-family collection includes guides for every model in that family. Individual model collections use exact slug matches. Collections unrelated to product families also use exact matches. Keep the wildcard scoped to the family so similarly named products do not enter the wrong collection.
- **Tags**: collections, products, hierarchy, groq

### collection-002: Collection Image System
Each collection has two image variants: `featuredImageUrl` (4:3, for topic tile cards on the hub) and `heroImageUrl` (16:9, for the collection page hero, text left, image right). Upload via `client.assets.upload('image')`.
- **Tags**: collections, images, featured, hero

---

## Build/UI Skills (retained: for ACE loop on website tweaks)

### build-001: Astro Template Customization Points
Eight customization points: (1) global CSS tokens, (2) the header component, (3) the footer component, (4) Astro configuration, (5) the Sanity client configuration, (6) base-layout typography, (7) hub hero text and collection mapping, and (8) taxonomy seed data.
- **Tags**: build, template, customization

### build-003: ACE Loop for Frontend at 9.8/10 HARD [PROTECTED]
Any change to the resource hub's Astro components, CSS, layouts, or copy goes through the ACE loop: Generator → Reflector → Curator. Repeat until the review reaches 9.8/10 or higher. The Reflector must provide exact file-and-line instructions stating what to change and what to replace it with. Measured Lighthouse results and axe scans are required evidence for clearing the threshold; the review score does not replace those checks.
- **Tags**: build, ace-loop, frontend, threshold
- **Status**: active [PROTECTED]

---

## Quality Skills (retained)

### quality-001: Playwright Self-Review After Every Deploy
Navigate to the deployed URL, authenticating if previews use Vercel Deployment Protection or Cloudflare Access. Capture screenshots at 1440px, 768px, and 375px. Check that cards render, filters work, series navigation renders, images load, audio has sources, and no placeholder text remains. Fix issues before reporting completion.
- **Tags**: quality, playwright, self-review, responsive

### quality-002: CDN Cache Awareness
After updating Sanity content, cached responses may still contain old data. Use `useCdn: false` during development when immediate freshness is needed. For production builds following content changes, verify freshness before building or fetch without the CDN. Creating a new client instance alone does not invalidate shared caches.
- **Tags**: quality, cdn, caching, sanity

### quality-003: Attribute Count Monitoring
After any schema-adjacent change, estimate the attribute count. Use fewer than 50 paths as a project design budget for a compact polymorphic model, not as a universal platform limit. Check current usage and limits in the project's Sanity management interface. Do not solve a tagging problem by adding document types; follow setup-002 and represent classification through the existing taxonomy model.
- **Tags**: quality, attributes, monitoring, limits

---

## NEW Maintenance/Vercel Skills

### vercel-mgmt-002: Sanity-Only Changes Don't Need Code Push
Pure Sanity content changes, such as adding a document, updating a taxonomy term, or changing a tag, do not require a code commit. Request-rendered pages can reflect the change after their caches refresh. Prerendered pages require a new build.
- **Vercel**: For prerendered content, trigger a deployment through the configured integration or run `vercel deploy --prod`. For request-rendered content, verify a fresh response after cache expiry or invalidation.
- **Cloudflare Workers Builds**: For prerendered content, trigger the configured deploy hook. For request-rendered content, verify cache behavior on the deployed Worker.
- **Both**: Check the site's rendering mode and cache settings before deciding whether a redeploy is needed. Verify the changed content at the deployed URL.
- **Tags**: vercel, sanity, redeploy, content-only

### handoff-mgmt-001: client_registry as Source of Truth
On startup, always read `05_automations/resource-hub-maintenance/runbook_appendix/client_registry.md` to identify registered sites and their maintenance scope. Never operate on an unregistered site. Complete setup or update its registration and deployment status before beginning maintenance.
- **Tags**: handoff, registry, scope

### handoff-mgmt-002: Defer First-Time Setup to the First-Build Automation
When asked to set up a new resource hub, redirect to the first-build automation:
> Use the first-build automation described in `05_automations/client-site-first-build/comprehensive_guide.md`. It handles the design handoff, Sanity bootstrap, repository, and hosting project. Resource-hub maintenance takes over content operations once the site has a stable preview and is registered.
- **Tags**: handoff, scope, redirect

### handoff-mgmt-003: Defer Test→Production Graduation to Website Maintenance
When asked to make a preview public or remove preview protection, defer to website maintenance:
> Follow `05_automations/website-maintenance/runbook_appendix/promote_to_production.md`. That process attaches the custom domain, removes preview protection where appropriate, updates Search Console, and runs a full Lighthouse audit.

Resource-hub maintenance does not remove preview protection or attach domains.
- **Tags**: handoff, scope, redirect

---

### wren-handoff-004: PLACEHOLDER_REMOVE_BEFORE_LAUNCH Marker Triggers Bulk-Delete [HANDOFF SEAM]

**Status**: active
**Tags**: handoff, placeholder, marker, bulk-delete, graduation, wren-handoff-004

**Rule**: The first-build process marks placeholder collections, resources, and taxonomies with `PLACEHOLDER_REMOVE_BEFORE_LAUNCH` in the `tags` array and `isPlaceholder: true`. These fields identify disposable preview content. Remove placeholder resources when real content enters their collection, and remove remaining placeholders before production promotion. If a placeholder collection or taxonomy becomes part of the real content structure, validate it and clear both placeholder markers before the launch cleanup.

**Fix-pattern (two trigger paths)**:

1. **Trigger Path A (first real resources land)**: When a Sanity API write adds one or more non-placeholder resources to a collection containing placeholders, immediately query for and delete that collection's placeholder resources, not the collection itself:
   ```groq
   *[_type == "resource" && (isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags) && references($collectionId)]
   ```
   Supply the target collection ID as `$collectionId`. Then bulk-delete through a single transactional `/data/mutate` POST. Report the actual number removed and the collection name.

2. **Trigger Path B (graduation signal, paired with scaffold-003-consume)**: When the user requests production promotion, query all remaining placeholder documents, including resources, taxonomies, and collections:
   ```groq
   *[_type in ["resource", "taxonomy", "collection"] && (isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags)]
   ```
   Complete the cleanup before handing the request to the website-maintenance production-promotion process.

**When to apply**: Every content-add operation on a site seeded with placeholders, and every production-promotion request. Where the tag marker is absent, use `isPlaceholder == true` to identify placeholders.

**How to apply (both paths)**:
1. Use the appropriate GROQ query above.
2. Count and inspect the matching documents before deleting them. Report the proposed scope, and check whether real content references any matched collection or taxonomy. Validate and retain adopted structures by clearing their placeholder markers before repeating the query.
3. Bulk-delete the remaining matches through a single transactional `/data/mutate` call, observing content-005 and the API's request limits.
4. Verify that the same GROQ query returns zero matches.
5. Report the result to the user.

**Anti-pattern 1**: Deleting the collection when only its placeholder resources should go under Trigger Path A. The collection's slug, name, and taxonomy relationships are still needed.

**Anti-pattern 2**: Skipping Trigger Path A and waiting until production promotion. This leaves placeholder resources mixed with real resources in previews and makes content reviews unreliable.

**Invented example**: A garden-supply shop's preview hub has placeholder collections for “Balcony containers” and “Compost basics.” Each contains a placeholder guide and carries the placeholder markers. When a real composting guide arrives, Trigger Path A removes the placeholder guide from “Compost basics” while retaining the collection. After validating the collection for real use, clear its placeholder markers. “Balcony containers” remains marked until it receives real content or is removed during production cleanup.

**Pairs with**:
- scaffold-003-consume: the required cleanup before production promotion; wren-handoff-004 also covers cleanup as real content arrives.
- handoff-mgmt-003: the production-promotion handoff occurs after Trigger Path B completes.

- **Severity**: HIGH (placeholder content can mislead reviewers and reach public pages if cleanup is missed)

---

## Cross-Propagated Skills (from First-Build Maintenance Lessons)

These skills carry lessons from `05_automations/client-site-first-build/skillbook.md` into resource-hub maintenance. They cover placeholder cleanup at handoff and visual verification when changing Astro components. When a canonical visual reference exists, compare the rendered result against it as part of the Reflector's measured checks.

### scaffold-003-consume: Maintenance MUST Bulk-Delete Placeholder Sanity Cards Before Graduation Hand-Off [GRADUATION PREREQUISITE]

**Origin**: First-build skillbook scaffold-003. Resource-hub maintenance consumes and verifies the handoff.

The first-build process may seed realistic but fictional Sanity documents using `isPlaceholder: true` and `tags: ["PLACEHOLDER_REMOVE_BEFORE_LAUNCH"]`. When the user requests production promotion, resource-hub maintenance must remove remaining placeholders before handing off domain attachment or preview-protection removal.

**Bulk-delete query (GROQ):**
```groq
*[_type in ["resource", "taxonomy", "collection"] && (isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags)]
```

**Procedure:**
1. Point every call at the correct project ID and dataset, read from the site's Sanity client configuration.
2. Run a read-only query to inspect and count deletion candidates:
   ```groq
   *[_type in ["resource", "taxonomy", "collection"] && (isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags)] { _id, _type, title }
   ```
   Check references from real content. Validate any collection or taxonomy adopted for real use and clear both placeholder markers before repeating the query.
3. Bulk-delete the remaining matches through a single transactional `/data/mutate` call within the API's request limits:
   ```python
   mutations = [{"delete": {"id": doc["_id"]}} for doc in placeholder_docs]
   ```
4. Verify that no placeholder markers remain:
   ```groq
   *[isPlaceholder == true || "PLACEHOLDER_REMOVE_BEFORE_LAUNCH" in tags] { _id }
   ```
   Resolve any remaining matches before continuing.
5. Only then report: “Placeholder documents are cleaned up. The site is ready for the website-maintenance production-promotion process.”

**Anti-pattern**: Never allow placeholder documents to reach public production. Check both Sanity records and rendered pages before promotion; a clean query alone does not prove cached or prerendered HTML is clean.

- **Tags**: graduation-prereq, sanity, bulk-delete, first-build-handoff, cross-propagated
- **Status**: active
### qa-010: Canonical Visual Diff is a P0 Reflector Gate When Canonical Exists

**Origin**: First-build visual-fidelity guidance, paired with scaffold-004.

When modifying a resource hub's Astro components through an ACE loop, if a canonical visual reference exists, the Reflector pass MUST include a canonical visual diff. The reference may be saved rendered HTML, a stylesheet, or an approved screenshot.

**Cheapest deterministic implementation:** Compare CSS tokens in the built stylesheets against the canonical stylesheet for a fixed list of design-critical selectors:

- The primary button and every call-to-action variant.
- The hero, the page header, and any tab or filter bar.
- Record the exact selectors for each site at first build; the list differs by design.

**Why this matters:** axe, Lighthouse, and AEO file-presence checks cannot detect visual fidelity changes. An accessibility fix can unintentionally recolor a key surface and drift from the approved design. Check both accessibility and visual fidelity. If they conflict, resolve the design explicitly rather than silently changing brand tokens or treating a visual match as proof of accessibility.

- **Tags**: ace-loop, reflector-rubric, visual-fidelity, canonical-diff
- **Status**: active

### ace-002-update: Empirical Reflector Gates MUST Include Canonical-Design Visual Diff if Canonical Exists

**Origin**: First-build ACE rubric guidance, paired with qa-010.

This is the rubric-level companion to qa-010 above. When running any modification that requires an ACE loop:

1. Check whether the site has a saved canonical design reference.
2. If yes, the Reflector's empirical checks MUST include a canonical visual diff, per qa-010.
3. If no canonical reference exists, use axe, Lighthouse, and agent-readiness checks as the baseline correctness rubric. Record that canonical fidelity could not be assessed.

Apply this alongside ace-002 and the existing 9.8/10 HARD threshold in build-003.

- **Tags**: ace-loop, reflector-rubric, canonical-diff, paired-with-qa-010
- **Status**: active

---

## Cookie Consent / Privacy

These skills describe repeatable patterns for cookie-consent setup and maintenance on a resource hub. The operational rules that follow apply to any ACE iteration on a site you maintain.

### cookie-consent-existing-wp-bridge-001 [PROTECTED]
When an Astro subdomain, such as `resources.example.com`, integrates with an existing WordPress site that has its own cookie management plugin, the subdomain MUST run a compatible bridge that BOTH reads the parent's consent cookie BEFORE rendering its own banner AND writes back to the parent's cookie format AFTER user action. This prevents repeated prompts during parent-to-hub-to-parent navigation and keeps consent choices consistent.

The bridge is a function pair: `bridgeFromWordPress`, called before `CookieConsent.run`, and `bridgeToWordPress`, called inside the `onFirstConsent`, `onConsent`, and `onChange` callbacks. Map the plugin's actual consent categories and values explicitly. Both functions must return early outside the configured production domain family to keep test environments isolated.

- **Tags**: cookie-consent, wp-bridge, cross-subdomain, consent-consistency, vanilla-cookieconsent
- **Status**: active [PROTECTED, recurring consent-consistency failure]

### cookie-consent-greenfield-001
When a banner is needed (port-027 in the client-site-first-build skillbook), one person or small team controls every property end-to-end, and no parent CMS plugin manages consent, use pure vanilla-cookieconsent v3. No bridge functions are needed. Greenfield means: (a) all properties share a consent implementation; (b) no parent WordPress, Drupal, or Joomla site sets a separate consent cookie; (c) the cookie can use the shared parent domain for cross-subdomain reuse.

Decision boundary: if even ONE property in the domain family uses an existing CMS consent plugin, use the bridge approach in `cookie-consent-existing-wp-bridge-001`, adapted to that plugin's format.

- **Tags**: cookie-consent, greenfield, vanilla-cookieconsent
- **Status**: active

### cookie-consent-decision-tree-001
**Scenario A vs B decision tree** for a cookie-consent setup. First decide whether a banner is needed at all: ship one only when something on the site needs consent (port-027 in the client-site-first-build skillbook). With cookieless analytics and no optional cookies, storage or tracking embeds, ship no banner and skip this tree. When a banner is needed:

- IF the parent domain already has a cookie management plugin → **Scenario A (bridge)**: the Astro subdomain runs vanilla-cookieconsent v3 with bridge functions compatible with that plugin. See `cookie-consent-existing-wp-bridge-001` and, for Cookie Notice, `wp-cookie-notice-bridge-pattern-001`. Keep the privacy notice unified on the parent, per `privacy-policy-unified-on-parent-domain-001`.
- ELSE → **Scenario B (greenfield)**: use pure vanilla-cookieconsent v3 with no bridge, per `cookie-consent-greenfield-001`. Put the privacy notice on the property itself.

Apply this decision during initial site discovery AND at the start of any cookie-consent maintenance task. Choosing the wrong scenario creates repeated banners when a bridge is missing or unnecessary coupling when no bridge is needed.

- **Tags**: cookie-consent, decision-tree, scenario-mapping
- **Status**: active

### vanilla-cookieconsent-cookie-domain-config-001
For cross-subdomain consent reuse, explicitly set the cookie's domain to the shared parent, such as `cookie.domain = 'example.com'`, in the vanilla-cookieconsent v3 configuration. A leading dot is also accepted by browsers but does not determine whether the cookie is host-only. Omitting the Domain attribute makes a cookie host-only.

A host-only cookie written on `resources.example.com` cannot be read by `example.com`, which can cause the banner to reappear during navigation. Use an `isCrossSubdomainCapable` guard that accepts only the configured parent hostname or its subdomains. Omit the shared domain on localhost and unrelated preview hosts so development uses a host-only fallback.

- **Tags**: cookie-consent, cookie-domain, cross-subdomain, vanilla-cookieconsent
- **Status**: active

### wp-cookie-notice-bridge-pattern-001
For a WordPress Cookie Notice installation that uses `cookie_notice_accepted`, map `'true'` to accepted, `'false'` to declined, and an absent cookie to undecided. Confirm those values and the cookie's actual domain in the installed plugin before implementing the bridge.

If the parent writes a host-only cookie, the subdomain cannot read it. Configure the WordPress side to write the cookie with the shared parent domain, path `/`, an appropriate expiry, `SameSite=Lax`, and `Secure` on HTTPS. Use the plugin's supported configuration or extension mechanism so its later writes do not undo the shared-domain setting. Remove conflicting host-only cookies during migration where necessary.

If the plugin cannot support shared-domain consent reliably, replace it with a compatible consent implementation. The Astro bridge handles reading and writing the agreed format; the WordPress configuration handles consistent cookie scope.

- **Tags**: cookie-consent, wordpress, cookie-notice-plugin, cross-subdomain, integration-handoff
- **Status**: active

### privacy-policy-unified-on-parent-domain-001 [SITE POLICY]
When integrating an Astro subdomain into an existing WordPress or CMS site with a shared privacy notice, link every privacy reference to the parent notice, such as `https://example.com/privacy-policy/`. Do not maintain a duplicate notice on the hub.

Reasons: (1) one source of truth for updates; (2) no content drift; (3) consistent descriptions of data handling across the parent and hub; (4) less confusion when visitors compare notices. Ensure the shared notice actually covers the hub's data handling. Centralize the URL in a `PARENT_PRIVACY_URL` constant used by every privacy link.

- **Tags**: cookie-consent, privacy-policy, unified-on-parent, site-policy
- **Status**: active [SITE POLICY, use the shared parent notice]

### cookie-consent-pre-allowlist-csp-001
When adding a cookie banner before analytics is connected, review the planned analytics integration and its CSP requirements at the same time. For an approved integration, prepare the required `script-src`, `connect-src`, and `img-src` entries so its later activation does not fail because the browser blocks its requests.

Keep an explicit purpose beside every allowed origin. Add only the origins required by the selected integration, and use wildcards only when necessary and documented. Do not allow every possible analytics vendor in advance. Verify both CSP behavior and consent-controlled loading when the integration is enabled; a prepared allowlist does not replace that check.

- **Tags**: cookie-consent, csp, forward-readiness, analytics, pre-allowlist
- **Status**: active

### cookie-settings-revisit-link-pattern-001
A footer link with `data-cc="show-preferencesModal"` lets visitors revisit consent preferences at any time without leaving the page. Keep the control easy to find so changing or withdrawing a choice is straightforward.

Pattern: `<a href="#" data-cc="show-preferencesModal">Cookie Settings</a>`. vanilla-cookieconsent v3 handles the click through its built-in event handling; no custom JavaScript is needed. Place the link in the footer's secondary navigation alongside Privacy Policy and Terms. Verify that preference changes also update any bridged consent state.

- **Tags**: cookie-consent, footer-link, preference-controls, vanilla-cookieconsent
- **Status**: active

---

## ACE Loop Operational Rules (PROTECTED, cross-loop)

These rules apply to any ACE iteration on a maintained site, including work unrelated to cookie consent. They protect against recurring process and verification failures.

### ace-loop-agent-discipline-001 [PROTECTED: recurring failure mode]
An ACE loop MUST use the formal `design-generator`, `design-reflector`, and `design-curator` agents. Generator builds → Reflector scores → repeat until SATISFACTORY ≥ 9.8/10 → Curator closes. Do not replace the agent loop with inline iteration or skip the Generator.

An artifact can appear correct while the process lacks a reproducible audit trail. The Generator must produce a generation report describing the changes, assumptions, and verification evidence. Without that report, the Reflector cannot reliably reconstruct what it is reviewing. This pairs with `build-003`: the 9.8 HARD threshold is meaningful only when the required review process produces it.

- **Tags**: ace-loop, agent-discipline, generator, reflector, curator, protected-recurring-failure
- **Status**: active [PROTECTED, recurring failure mode]

### browser-automation-tool-decision-001 [PROTECTED]
Browser automation tool decision tree:

1. **Headless Playwright via Node script**: DEFAULT for programmatic verification, including cookies, network requests, assertions, axe-core injection, and computed-style measurements. Use `chromium.launch`; pass `executablePath` only when using Chromium other than the bundled version. When testing a banner configured with `hideFromBots: true`, apply `await context.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));` before navigation so the test can exercise the visitor-facing banner. Document this test-only override.
2. **Node CLI with Playwright**: alternative for a one-shot JavaScript evaluation against a deployed URL when Playwright is already installed. Keep the invocation small and record its result.
3. **Playwright MCP**: reserve for visual inspection, screenshots, and exploratory probing. Use a Node script for repeated assertion-driven checks so they remain straightforward to rerun.

A visual claim that a banner renders is insufficient if the standard headless test cannot reproduce it. Bot-hiding settings can suppress the banner before any interaction occurs. Record the relevant configuration and test setup so another run reaches the same state. A reusable harness is described in `05_automations/resource-hub-maintenance/runbook_appendix/playwright_cookie_test_harness.md`.

- **Tags**: browser-automation, playwright, headless, navigator-webdriver-override, mcp-decision-tree, protected
- **Status**: active [PROTECTED]

---
## Reflector-Graduated Skills from Cookie-Consent Testing

These skills capture reusable lessons from cookie-consent testing and review. Apply them across site builds and resource-hub maintenance.

### vanilla-cookieconsent-v3-prefs-modal-uses-class-not-id-001 [TESTING]
vanilla-cookieconsent v3 preferences modal uses class `.pm`, not id `#pm`. The banner uses class `.cm` with an `id=cm` wrapper. Tests verifying preferences-modal opening MUST select via `document.querySelector('.pm[role=dialog]')` OR `document.querySelector('div[role=dialog][aria-modal=true]')`. Checking `document.getElementById('pm')` returns null even when the modal is fully rendered and visible. Version-specific markup and options such as `hideFromBots` can defeat naive assertions. Check the rendered DOM and test configuration before treating a missing selector as a product failure. Pair with `browser-automation-tool-decision-001` and the guidance in `05_automations/resource-hub-maintenance/runbook_appendix/playwright_cookie_test_harness.md`.
- **Tags**: cookie-consent, vanilla-cookieconsent, playwright, testing, false-negative-trap
- **Status**: active [protected-candidate]

### axe-truncation-unmasking-redirect-block-001 [QA: route-scoped scanning]
When scanning a route with a client-side redirect, such as a `setTimeout`-driven `location.replace`, the test harness MUST block the redirect to scan the intended page content. Direct override of `window.location.replace` fails because it is a non-configurable native property. For timer-driven redirects, wrap `setTimeout` before page scripts execute, inspect the callback's string representation for redirect substrings (`'window.location.replace'`, `'location.replace'`, `'location.href'`), and return `-1` to swallow a matching timer. Combine this with removal of `meta[http-equiv=refresh]` elements on `readystatechange`. This is a targeted test technique; verify that it catches the route's actual redirect mechanism. Without redirect blocking, a thank-you route can surface a false `html-has-lang` violation when axe scans a destination error page, while masking real color-contrast violations on the intended page. Confirm the URL and rendered content before accepting scan results. Apply this discipline to any Playwright and axe-core stack.
- **Tags**: qa, axe-core, playwright, redirect-block, setTimeout, route-scoped-scanning
- **Status**: active [protected-candidate]

### aa-token-suffix-naming-convention-001 [CONVENTION]
When introducing AA-cleared sibling tokens to fix WCAG contrast violations in a brand-color system, use the suffix `-aa` and name tokens by their role, not their hue, such as `--brand-primary-aa` next to `--brand-primary`. Convention benefits: (1) future maintainers can search for `-aa` to find contrast-related swaps; (2) original brand tokens remain available for decorative surfaces that do not convey information; (3) the relationship between the original and its AA derivative is explicit in the name; (4) text and decorative selectors can use separate tokens without collisions. PAIR WITH: a code-comment block at each consuming selector citing the measured contrast ratio, background color, and this skill ID. For an invented ceramic studio (these hex values are invented for illustration), `--brand-primary: #7A9CC6` measures about 2.8:1 on white, so text gets `--brand-primary-aa: #2E5A87` (about 7.2:1); `--accent-secondary: #B8954A` (about 2.8:1) gets `--accent-secondary-aa: #6B4E16` (about 7.7:1). Compute the ratio for each actual foreground/background pair with the WCAG relative-luminance formula or a contrast checker, then limit swaps to the surfaces requiring correction. A suffix alone does not establish accessibility.
- **Tags**: conventions, wcag, aa, css-tokens, brand-tokens, naming-convention
- **Status**: active

### selector-color-only-swap-vs-structure-change-discipline-001 [PATTERNS: preserving shared chrome structure]
When a protected design requirement says to preserve shared header and footer STRUCTURE and AA clearance is needed, use this surgical fix discipline: (1) change only color VALUES in existing `:root` variables, without renaming tokens that other selectors consume; (2) do not add layout, dimension, or positioning changes; (3) when a single CSS rule combines persistent and transient states, such as `.a, .a:hover, .a:focus`, split the persistent state into its own rule for a color-only override; (4) document the split with a code comment identifying the structural requirement and the reason. Preserve the existing hover and focus colors only where they also meet the applicable contrast requirements. A default axe scan does not establish their accessibility. For an invented regional bakery chain (values invented for illustration), a footer-pill token could change from `#9FB8D0` (about 2.1:1 with white text) to `#2E4A66` (about 9.2:1) where white text requires stronger contrast, while `.site-nav-link.is-active` receives a separate text-color rule. Keep `.site-header`, `.site-footer`, `.site-logo`, and `.site-nav-list` structurally unchanged. This preserves layout and interaction cues while correcting contrast.
- **Tags**: patterns, wcag, aa, chrome, css-discipline, structural-preservation
- **Status**: active [protected-candidate]

---

### atomic-mutate-batch-001
Use a single atomic `/data/mutate` POST containing `createOrReplace` operations for all required taxonomies and resource documents in one transaction. Avoid separate single-document create calls for an update that must succeed or fail together: they add request overhead and can leave partial content behind. SDK pattern: `const tx = client.transaction(); for (const t of taxonomies) tx.createOrReplace(t); for (const r of resources) tx.createOrReplace(r); await tx.commit();`. Deterministic document IDs are mandatory for idempotency. Derive resource IDs from a stable resource key and taxonomy IDs from a stable category-and-term key, using distinct namespaces. Repeating the batch must address the same documents. Use `createOrReplace` only when the supplied document is the intended complete replacement. Resource `taxonomies[]` entries use `{_type: 'reference', _ref: <doc-id>, _key: <unique-array-key>}`; keep array keys stable across reruns where possible.
- **Tags**: atomic-mutate, sanity-mutate, idempotency
- **Status**: active

### featured-flag-3card-grid-001
Editorial Featured checkbox → Sanity `resource.featured` boolean → Astro `resources.filter(r => r.featured).slice(0, 3)`. For a kitchen-equipment maker's resource library using this layout, mark exactly 3 resources Featured to fill the homepage's 3-card grid. If none are featured, fall back to a single configured card pointing to the library introduction. If more than 3 are featured, sort by `publishedDate` descending before taking the first 3. Each card derives its type from the primary taxonomy with `category='format'`, title and description from `r.title` and `r.abstract`, and href from `externalUrl`, then the resource detail URL, then `#` as an incomplete-data fallback. Resolve incomplete links before publishing. Accent colors cycle through the site's role-named accent tokens by index; CTA text comes from `TYPE_CTAS`. When present, `featuredImage` renders as an `<img>` over the accent placeholder.
- **Tags**: featured-cards, canonical-pattern, 3-card-grid
- **Status**: active

### type-labels-cta-dict-001
Maintain two parallel dictionaries beside the `toCard` helper in the homepage's Astro frontmatter: `TYPE_LABELS` maps taxonomy slugs to display labels for badges and metadata, and `TYPE_CTAS` maps those slugs to action text. Keys must cover every resource type in the site's editorial schema. For an invented bicycle-repair co-op's guides, examples include `repair-guide` → 'Repair Guide' / 'Read the guide', `repair-video` → 'Repair Video' / 'Watch the video', `parts-list` → 'Parts List' / 'View the parts list', `workshop-recording` → 'Workshop Recording' / 'Watch the recording', and `member-story` → 'Member Story' / 'Read the story'. Keep each slug and its label naming the same thing. Match the verb to the destination: a detail page should not promise an immediate download. Default fallback: 'Resource' / 'View the resource'.
- **Tags**: type-labels, cta-verbs, canonical-dict
- **Status**: active

### sanity-polymorphic-arbitrary-fields-001
A polymorphic content model using `resource`, `taxonomy`, `collection`, and `series` document types can store additional fields through the `/data/mutate` API without first adding Studio editor definitions. To add a field, include it in the mutation and project it through GROQ in the read helpers. Astro pages can use the field once their queries, types, and rendering support it. A purely additive field does not require a database schema migration, though existing documents may need backfilling. To expose it in Studio, update the Studio schema; that editor change is optional when another supported editing interface owns the field. For an invented garden-supply shop, fields such as `authorName`, `estimatedReadMinutes`, `seasonLabel`, `gated`, and `featuredImage` can be introduced this way. Validate their shape at the write boundary because API storage does not enforce the Studio's editorial validation rules.
- **Tags**: sanity-polymorphic, arbitrary-fields, no-schema-migration
- **Status**: active

### card-image-dimensions-001
Canonical card image specs for hubs using this pattern. Featured cards (`.feat-card-img`, 3-card homepage grid): aspect ratio 16:10 at all breakpoints. Recommended export: **1200×750 px**. Resource list cards (`.res-card-img`, library cards): 16:11 desktop at 220px wide, changing to 16:9 mobile below 680px. Recommended export: **1200×675 px**, prioritizing mobile because it displays the larger image. Format targets: WebP at quality 80, ideally 40–80 KB; JPEG at quality 85, approximately 120–200 KB. Actual size depends on image content. Use PNG when lossless detail is necessary, such as small text that degrades under lossy compression. Both `.feat-card-img img` and `.res-card-img img` use `width: 100%; height: 100%; display: block; object-fit: cover;`. Store exports in the project's public asset directory with stable, descriptive names and keep the resulting URL in the resource record.
- **Tags**: card-dimensions, canonical-spec, image-pipeline
- **Status**: active

### astro-card-rendering-conventions-001
Canonical Astro rendering for a Sanity-driven resource library. Two card sections: (1) Featured 3-card grid uses `.feat-card`, `.feat-card-img`, `.feat-card-body`, and `.feat-card-cta` classes, with a 16:10 image and prominent CTA. (2) All-resources library list uses `.res-card`, `.res-card-img`, `.res-card-body`, and `.res-card-cta` classes, with a 16:11 desktop image, 220px thumbnail, body, and right-side CTA pill. Both card types support an accent-color placeholder when no image exists, cycling through role-named values such as `data-accent='primary|secondary|tertiary'`, and an `<img>` child when a `featuredImage` URL is present, using `object-fit: cover`. External URLs get `target='_blank' rel='noopener noreferrer'`; internal resource detail links do not. For an invented ceramic studio, the `.res-card` metadata line includes the type label, primary product taxonomy, primary skill-level taxonomy, and year derived from `publishedDate`. Render a `.library-empty` div when there are no resources. The `toCard` helper converts a Sanity resource into a card view-model with `type`, `typeSlug`, `title`, `desc`, `href`, `accent`, `cta`, `featuredImage`, and `gated` fields.
- **Tags**: astro-rendering, card-conventions, canonical-pattern
- **Status**: active

---

## Library Filter UX & Slug Pages

### sidebar-4-category-structure-001
For an invented garden-supply shop using this four-category pattern, the All Resources sidebar has exactly 4 accordion categories: **Resource Type · Product · Project · Skill Level**, in that order. Each maps directly to an editorial field and a Sanity taxonomy category: `format`, `product`, `project`, and `experience`. Use one agreed mapping throughout ingestion, queries, cards, and filters. Do not mix superseded categories into the sidebar; migrate old tags into the current model first. Astro frontmatter computes per-option counts server-side via `pristineCount(cat, slug)` and renders the sidebar via `FILTER_CATEGORIES.map`. Each `.filter-item` gets `data-cat` and `data-slug` attributes plus a `<span class='count' data-pristine={n}>(N)</span>` beside its label. Each `.res-card` gets `data-tags='cat:slug cat:slug ...'`, with space-separated tags, and `data-search='<lowercased haystack>'` for browser-side filtering and search.
- **Tags**: sidebar-filters, 4-categories, canonical-pattern, reusable
- **Status**: active

### filter-sidebar-dimming-pattern-001
Three states per filter option:

1. **PRISTINE** (no filters active, no search): options with 0 matching resources are hidden entirely (`.filter-item--empty` → `display: none`). Categories whose options are all zero are hidden too.
2. **ACTIVE-FILTERS or SEARCH**: options with 0 matches under the current cross-category constraints remain visible but dimmed (`.filter-item--dimmed` → `opacity: 0.45; cursor: not-allowed`). Count shows `(0)`. If selection is unavailable, enforce that behavior in the control as well as its styling.
3. **CHECKED**: always render at full opacity regardless of count. Never remove the user's explicit selections or prevent their deselection.

**Cross-category counting** uses OR within a category and AND across categories. For option `(cat, slug)`, count resources that match the search, match all active filters in other categories, and carry this `(cat, slug)` tag. Exclude same-category filters from the count predicate so each option shows its own matching resources under the other constraints. This count is not necessarily the total result count after adding the option, because OR selections can overlap. `applyFiltersAndSearch` iterates cards to set `display: none` or restore their display, then iterates filter items to update count `textContent` and dimmed/empty classes. An initial pass on script load establishes the pristine state.
- **Tags**: dimming-pattern, sidebar-filters, ux-canonical, cross-category-counting
- **Status**: active
### slug-detail-page-every-resource-001
Generate a detail page for EVERY Sanity resource, including file-only entries. Restricting detail pages to resources with `htmlContent` can leave spec sheets and other downloads with missing detail URLs. Use `getStaticPaths` with `resources.map(r => ({params: {slug: r.slug.current}}))` after validating that every resource has a unique slug. The detail page handles all combinations gracefully: (a) full HTML content if `r.htmlContent` is set, (b) Download/View resource action buttons if `fileUrl`/`externalUrl` is set, (c) fallback message "This resource is being prepared for the library" when neither content nor a link target is available. Cards still link directly to `externalUrl` OR `fileUrl` when present, and fall back to `/resources/{slug}` when neither exists. Verify that every resource detail URL resolves and that its structured data is valid. Apply this pattern to every Sanity-driven resource hub.
- **Tags**: slug-page, getStaticPaths, 404-fix, canonical-pattern
- **Status**: active

### tocard-href-precedence-001
The Astro `toCard` helper that converts a Sanity resource to a card view-model derives href via this precedence: **(1) `r.externalUrl`** if set (customer story, YouTube, external PDF on the business's main site) → **(2) `r.fileUrl`** if set (Sanity asset upload, direct PDF/file link) → **(3) `/resources/{slug}`** if `r.slug?.current` exists (internal detail page) → **(4) `#`** as final fallback. Including `fileUrl` means resources with Sanity-uploaded assets but no external URL link directly to the file, avoiding an unnecessary wrapper page. External URLs render `target='_blank' rel='noopener noreferrer'`; internal `/resources/{slug}` links do not. Keep this precedence in a shared `resourceHref` function used by `toCard`.
- **Tags**: tocard-helper, href-precedence, fileUrl, canonical-pattern
- **Status**: active

### gating-disabled-default-001 [DEFAULT POLICY]
By default, NO resources are routed through a gated form-fill flow. Where a build includes gated detail routes, a thank-you redirect chain and a `GATED_RESOURCES` registry, keep those mechanisms intact. Disable gating by removing home-page href links to gated routes.

**Re-enable for any specific resource via 4 steps**:
1. Add an entry to `GATED_RESOURCES` with title/subtitle/type/bullets/assetUrl/formProvider/provider-config.
2. Add the slug to the gated route's static slug collection, such as `STATIC_SLUGS`.
3. Set the desired card's href to `/resources/gated/<slug>` through a hero CTA, hero card, featured grid or Sanity resource document's `externalUrl`.
4. Configure the form provider's redirect-after-submit to `/resources/gated/<slug>/thank-you`.

**WHY default-off**: a business may choose lead capture for selected downloads, but a form adds friction to content discovery. Default-off with a straightforward enable path keeps ordinary resources accessible while supporting deliberate exceptions.
- **Tags**: gating-disabled, public-access, default-off, resource-configuration
- **Status**: active [DEFAULT POLICY]

---

### sanity-asset-upload-resource-patch-001
Per-attachment workflow: (1) Upload via `client.assets.upload(assetType, stream, {filename})` where assetType='file' for PDFs/docs and 'image' for images. Sanity returns `{_id, url}`. (2) Patch fields: for fileAsset → `{fileAsset: {_type: 'file', asset: {_type: 'reference', _ref: <asset-id>}}}`; for featuredImage → `{featuredImage: <asset-url>}`. (3) Apply via `client.transaction` with `tx.patch(resourceId, p => p.set(fields))` then `tx.commit`, atomic across all resource-document patches. Asset uploads happen before this transaction. (4) The GROQ resource query exposes the file URL: `"fileUrl": fileAsset.asset->url`. (5) Cards consume it via `toCard` href precedence (`externalUrl → fileUrl → /resources/{slug} → #`). Sanity deduplicates identical uploaded content by hash, allowing existing assets to be reused. Its CDN serves assets with edge caching.
- **Tags**: sanity-assets, asset-upload, resource-patch, canonical-pattern
- **Status**: active

### taxonomy-display-title-case-001 [PROTECTED: DISPLAY CONVENTION]
Every Sanity taxonomy document stores: (1) **TITLE** as a **Title Case + space-separated** human-readable label, such as "Care Guide", "Wheel Parts" or "Commuter Setup" for an invented bicycle-parts company's guide library; (2) **SLUG** as kebab-case lowercase, such as "care-guide", "wheel-parts" or "commuter-setup"; (3) **ID** in a deterministic format such as `facet.<category>.<slug>`. The TITLE appears in the sidebar and card metadata. **NEVER store the slug as the title**, which can create duplicate-looking labels such as "care-guide" and "Care Guide". For type-category taxonomies imported from lowercase, dashed values, ALWAYS use an explicit display-title map. For product, topic and use-case categories, preserve source titles only after confirming that they follow the display convention. The ingestion mapping and Astro display mapping MUST stay in sync, preferably by sharing one definition.
- **Tags**: taxonomy-display, title-case, canonical-pattern, display-convention
- **Status**: active [PROTECTED, DISPLAY CONVENTION]

### taxonomy-dedup-cleanup-procedure-001
When a sidebar shows duplicate-looking facets, such as "planter-care" AND "Planter Care" in a garden-supply shop's how-to hub, check for seeded and imported taxonomies sharing the same kebab-case slug but different IDs or titles. Use one atomic transaction for remediation: (1) Audit via GROQ, `*[_type=='taxonomy']{_id, title, slug, category, "refCount": count(*[_type=='resource' && references(^._id)])}`. (2) Identify duplicate pairs by matching `slug.current` within the same category. (3) Choose the canonical ID using the site's deterministic format, such as `facet.<category>.<slug>`. (4) For each duplicate pair, keep the canonical document, patch its title to Title Case, repoint references from the duplicate to the canonical document, then delete the duplicate. (5) Delete unused legacy taxonomies with no canonical pair only after confirming that no other document types reference them. (6) Submit the reference patches, title patches and deletes in one `tx.commit`. Re-run the audit after committing. The GROQ reference-count subquery identifies resource usage; extend the check if other document types can reference taxonomies. Pairs with `taxonomy-display-title-case-001`. Resolve duplicate identities BEFORE applying title-case fixes so you only patch the canonical document.
- **Tags**: taxonomy-dedup, cleanup-procedure, sanity-mutate, canonical-pattern
- **Status**: active

### resource-file-completeness-audit-001
After any source-to-Sanity ingest run, EMIT a per-resource audit table and summary showing: (a) total resource records, (b) count with `externalUrl`, (c) count with a resource file attachment, (d) count with a featured image attachment, (e) count with NO direct link target, meaning neither `externalUrl` nor `fileAsset`. Flag every "NO LINK TARGET" row so the site maintainer can add an external URL, upload a file or confirm that an internal content page is intentional. Include the audit in both the run log and the site's maintenance record. Do NOT skip it even if all uploads succeed: successful transfers do not prove that every expected resource has content and a usable destination.
- **Tags**: audit-required, completeness-check, mandatory-step, canonical-pattern
- **Status**: active

---

## UI Tweak: shared defaults (canonical for every hub built from this pattern)

### cta-articles-less-canonical-001 [PROTECTED: CTA CONVENTION]
All resource-hub card CTAs MUST be article-LESS, with no "the", "a" or "an". Pattern: `<verb> <noun>`, allowing a necessary preposition. Examples for a ceramic studio's library: "Read guide", "Download datasheet", "Watch video", "Listen to podcast", "Read customer story". Applies to the `TYPE_CTAS` dictionary, the `toCard` fallback string ("View resource"), hardcoded fallback featured cards and ANY hero CTA buttons. SUPERSEDES the CTA portion of `type-labels-cta-dict-001`; the `TYPE_LABELS` map is unchanged. Apply this convention to both first-build defaults and later resource additions.
- **Tags**: cta-canonical, article-less, display-convention, reusable-pattern
- **Status**: active [PROTECTED, CTA CONVENTION]

### resource-hub-ui-minimalism-bundle-001 [SHARED DEFAULT: 8 atomic patterns]
Bundle of 8 minimalism patterns: (1) **page-header-title-only**, h1-only header with a short noun; remove the subtitle and bottom rule; reduce excess padding while retaining readable spacing. (2) **featured-section-h2-only**, drop the eyebrow and introductory curation paragraph; use the literal h2 label "Featured Resources" in the site's heading font at weight 700. (3) **library-section-no-eyebrow-no-desc**, make the All Resources section title-only. (4) **hero-card-image-only**, use a `.hero-card--image-only` modifier to remove the body row; the image fills the full card; preserve aspect-ratio 4/5. (5) **hero-meta-removed**, remove file-length and format metadata from the hero. (6) **library-search-no-kbd-hint**, remove the `<kbd>/</kbd>` badge while retaining the keyboard binding. (7) **library-no-results-count-no-sort**, remove the resource count and sort control; sidebar filters and search support discovery; default to `publishedDate` descending. (8) **res-card-meta-no-redundant-type**, remove the leading resource-type span because the corner badge already identifies it; retain product or topic and year, such as a regional bakery chain's product range and guide year. Apply all 8 patterns to the first-build scaffold and subsequent UI maintenance.
- **Tags**: ui-minimalism, shared-default, canonical-pattern, reusable-pattern
- **Status**: active [SHARED DEFAULT]

### body-font-weight-400-not-300-canonical-001 [drift-fix discipline]
Body text uses font-weight: 400 (Regular), NOT 300 (Light). Establish explicit typography and colour tokens, then check for drift during every UI change: H1 weight 700 rather than 600 when that is the chosen heading standard; body colour from the body-ink token rather than an arbitrary black; no pale accent colour for body-size text on white when its contrast is insufficient. A 3.6:1 contrast ratio meets AA for large text only; normal-size text needs at least 4.5:1. Use a darker accessible token for body copy. For an invented kitchen-equipment maker using a charcoal and terracotta palette, apply the accent consistently to CTAs and draft banners while checking each text/background pair. Other drift points include pull-quote versus dek treatment, H2 top margins and rule borders, full-bleed hero alignment using the 100vw and 50% offset technique, and eyebrow colour on dark backgrounds. Maintain a short list of the site's chosen treatments and check it on every UI tweak.
- **Tags**: drift-fix, font-weight-400, quality-check, design-tokens
- **Status**: active

---

## Strict-Fidelity Blog/Page Recreation: multi-agent workflow

Use this skill cluster when supplied **pristine HTML/Markdown blog posts or static pages** must be recreated faithfully in an Astro build and registered in Sanity CMS. This is a preservation task, distinct from drafting new content or adapting its voice. Preserve source content exactly; account explicitly for integration changes such as asset URLs, CSS scoping and framework markup. Do not claim byte-identical output if those changes alter the rendered document.

**Trigger phrases**: "Here's a pristine HTML blog post, recreate it byte-for-byte" / "I'm handing you N blog posts, lift each one verbatim" / "absolute fidelity recreation" / "perfect accuracy when this goes live" / "absolute recreation" / "byte-faithful" / "byte-strict".

### strict-fidelity-blog-html-recreation [PRESERVATION PATTERN]
When a user supplies pristine HTML/Markdown and requests exact recreation, use parallel design-generator agents for independent pages, with batch size limited by available capacity. Review each page with a design-reflector using empirical checks: paragraph count, heading hierarchy, image alt text, source URLs, smart quotes, AEO schema preservation, reading-time accuracy, asset placeholder presence and rendered CSS scope classes. For multiple pages, add a final cross-page review covering taxonomy consistency, related-content links, Sanity slug uniqueness, AEO consistency, featured-image fallback order and source-record field completeness.

Resource-hub integration also requires: (a) bind captured images to Sanity CDN assets, or retain an explicit `{{ASSET:identifier}}` placeholder with `data-original-url` until binding is complete; unresolved placeholders must be visible in the review report; (b) preserve JSON-LD blocks as a STRING ARRAY per `sanity-attribute-name-no-at-prefix-001`; (c) compute reading time from the preserved prose word count; (d) use one generic slug-based Astro resource renderer instead of a dedicated file for each post; (e) wrap each rendered body in `.<slug>-blog` and scope content CSS selectors to that wrapper, preserving the source layout and styling within it; (f) submit the Sanity document writes as one atomic `/data/mutate` POST per `atomic-mutate-batch-001`; (g) default gating state to public per `gating-disabled-default-001`. Verify the live rendered result as well as stored source content, since successful ingestion alone does not prove faithful presentation.
- **Tags**: strict-fidelity, html-recreation, multi-agent, parallel-batches, sanity-cms, image-asset-binding, aeo-preservation, source-preservation
- **Status**: active [PRESERVATION PATTERN]
### sanity-attribute-name-no-at-prefix-001 [UNIVERSAL]
**Rule**: Store JSON-LD in Sanity as an **array of strings**, where each string is the `JSON.stringify` output of one JSON-LD object. Do not store JSON-LD as nested Sanity objects. Sanity attribute names must start with a letter or underscore, so keys such as `@context`, `@type` and `@id` are rejected when written as object fields. At render time, emit each string unchanged inside its own `<script type="application/ld+json">` element.
- **Why**: a string array keeps every JSON-LD key exactly as written, and the page outputs the same text the editor stored.
- **Verify**: after a write, read the document back and parse each string with `JSON.parse`; then confirm the built page contains one `application/ld+json` script per stored string.
- **Tags**: sanity-cms, json-ld, aeo-preservation, schema-storage
- **Status**: active

### multi-blog-cross-consistency-final-reflector [NEW SEED]
When **2 or more blogs** are handed over in a single strict-fidelity recreation batch, dispatch a **final high-level design-reflector** AFTER the per-page Reflectors pass. This final Reflector audits cross-blog properties that per-page Reflectors cannot see: (1) **taxonomy tag consistency**, every blog reuses existing taxonomy slugs, with no unreviewed variants such as "wheel-care", "wheel-maintenance", and "maintaining-wheels" for the same bicycle-parts topic; (2) **related-content link graph integrity**, internal links between the new blogs resolve to slugs that exist in the batch OR in the existing Sanity dataset, with no dangling resource-detail links; (3) **Sanity slug uniqueness**, no two blogs in the batch share a slug, and none collide with existing Sanity documents, verified with GROQ; (4) **AEO consistency**, JSON-LD Person/Organization references use the SAME canonical author and organization URLs across all blogs in the batch; (5) **featured-image integrity**, each blog has a resolvable featured image selected according to the site's documented image precedence, and no base64-embedded images remain; (6) **editorial-record completeness**, if canonical content came from an editorial database, every required field is populated and the import reads all canonical fields. **The larger the batch, the more important this shared review becomes.** NEVER skip when the batch contains 2 or more blogs; per-page Reflectors cannot catch these cross-blog issues.
- **Tags**: strict-fidelity, final-reflector, cross-blog-consistency, taxonomy, link-graph, slug-uniqueness, aeo, featured-image-integrity, editorial-record-completeness
- **Status**: active [NEW SEED]

### html-canon-wins-over-brand-voice-on-strict-mode [NEW SEED]
In strict-fidelity HTML recreation, **brand-voice transformations are SUPPRESSED**. Preserve the canonical HTML's voice verbatim, including every paragraph, sentence, punctuation mark, ellipsis, and footnote marker. No editorial smoothing. No header-case normalization. No paragraph merging. No tone shift to match the site's brand voice. Brand-voice alignment applies ONLY when writing new content. **Trust the canonical source; do not impose interpretation.** If a ceramic studio's source uses "hand-built", do not normalize it to "handbuilt"; preserve punctuation spacing; if the source uses British spelling such as "colour", do not convert it to "color". Per-page Reflector checks must verify paragraph counts, compare preserved punctuation byte-for-byte, and confirm the exact heading hierarchy. Reject any revision that introduces editorial interpretation. Discriminator: "Write a new blog about <topic>" → creative writing, with brand-voice transformations APPLIED. "Recreate this HTML blog byte-for-byte" → strict-fidelity recreation, with brand-voice transformations SUPPRESSED. When in doubt, ask the user which mode applies before dispatching the generator agent.
- **Tags**: strict-fidelity, creative-writing, mode-discriminator, brand-voice-suppressed, byte-strict, source-fidelity
- **Status**: active [NEW SEED]

### inherited-from-first-build-multi-agent-rebuild [PROTECTED: inherited capability from client-site-first-build]
**INHERITED capability** from the [first-build skillbook](05_automations/client-site-first-build/skillbook.md). The multi-agent rebuild pattern supports first-build scaffolding from a canonical HTML handoff, recreation of blogs on existing resource hubs, and verification before promotion to production. This entry defines how those responsibilities divide across the automations. **Resource-hub maintenance scope**: (a) blog and static-page recreation on an already-deployed resource hub; (b) Sanity CMS registration using a shared dynamic resource-detail renderer; (c) image asset binding to the Sanity CDN; (d) AEO schema preservation; (e) public access by default unless restricted access is explicitly requested. **What resource-hub maintenance does NOT inherit**: first-build scaffold creation, including repository and hosting-project creation, initial schema deployment, and initial requirements gathering. **Website-maintenance verification scope**: an editorial HTML budget of 200 KB; Lighthouse Performance >=85, LCP <=2.5s, and CLS <=0.1; CSS scoped to the appropriate content wrapper; and Sanity attribute naming consistent with `sanity-attribute-name-no-at-prefix-001`.
- **Tags**: inherited-capability, strict-fidelity, multi-agent-rebuild, resource-hub-scope, website-maintenance-scope, protected, cross-automation
- **Status**: active [PROTECTED, inherited from client-site-first-build]

---

### editorial-canonical-css-global-stylesheet-architecture [PROTECTED, USER DIRECTIVE]


**Cross-references**: `global-css-scope-templated-only-local-handauthored` defines the required selector scope for the shared stylesheet.

**Body**: When per-page `htmlStyles` is set to an empty string because the global stylesheet is expected to cover canonical classes, VERIFY that the global stylesheet actually covers EVERY canonical class, not just the recently added subset. A template retrofit can remove all per-page styling while transferring only card and CTA rules into the shared stylesheet. Missing rules may include the resource header, title, metadata, introduction, summary, guide body, document viewer, video and audio embeds, listening links, transcript, source attribution, explanatory sections, print styles, responsive breakpoints, and theme-token CSS variables. Clearing `htmlStyles` before transferring these rules leaves those elements unstyled.

**Architectural fix**: replace repeated per-page CSS with one complete global ruleset for templated editorial pages. Transfer the full canonical CSS, including responsive and print behavior. Scope it to the template-only wrapper described below. Once coverage is verified, generators can emit `htmlStyles: ""`.

**Generator contract**: `htmlStyles: ""` is correct in the Sanity content patch for a templated page whose canonical classes are fully covered. Do NOT write per-page CSS for shared canonical classes; this creates duplicate rules across documents. If a NEW canonical class needs styling and is absent from the global stylesheet, ADD it to the shared ruleset under a clearly labeled templated-editorial-styles comment.

**Reflector contract**: verify that `htmlStyles` is an empty string for templated pages. If it is non-empty, verify that the rules are page-specific rather than generic canonical styling that belongs in the shared stylesheet.

**Forward-applicable to any site**: substitute the site's theme-token CSS variables. One complete shared stylesheet per site allows all templated editorial pages to render correctly with empty per-page `htmlStyles`.


---

### global-css-scope-templated-only-local-handauthored [PROTECTED, USER DIRECTIVE]


**Cross-references**: `editorial-canonical-css-global-stylesheet-architecture` establishes shared CSS coverage; this entry defines its scope.

**The architectural rule** (CRITICAL, apply consistently):

Two content categories live inside the shared dynamic resource-detail renderer's outer wrapper:

| Category | Examples | Styling source |
|---|---|---|
| **TEMPLATED editorial patterns** (generated from a file or external-link source) | kitchen-equipment spec sheet, bicycle-parts guide, garden-supply case study, video embed, audio embed | GLOBAL stylesheet, scoped to `[class*="resource-page-pattern-"]` |
| **HAND-AUTHORED content** (built from scratch without a file or external-link source) | ceramic studio blog, bakery story, custom page, topic page, hand-authored customer story | LOCAL per-page `htmlStyles`, untouched by global editorial rules |

**The enforcement mechanism**: scope all global editorial CSS to `[class*="resource-page-pattern-"]`, a wrapper class present ONLY on templated pages and ABSENT on hand-authored content. Keep local page rules scoped to their own page wrapper as well. This prevents template rules from matching hand-authored pages.

**ANTI-PATTERN that this prevents**: scoping global editorial CSS to the shared Astro outer wrapper. Hand-authored content also lives inside that wrapper, so global rules at that scope leak into its design and override it. Fix the regression by rescoping every shared editorial selector to the template-only wrapper.

**Generator/reflector contract**:
- When emitting per-page `htmlStyles` for hand-authored content, scope rules to that page's wrapper. It must not carry a `resource-page-pattern-` class.
- When generating templated editorial pages, emit `htmlStyles: ""` and rely on the global stylesheet. A wrapper such as `<div class="wheel-care-page resource-page-pattern-guide">` MUST be present as the `htmlBody` outer div.
- Reflector check: verify that global editorial CSS edits target a wrapper exclusive to templated pages. Flag REFINE if a rule could leak into hand-authored content.

**Forward-applicable to every site and automation that writes global CSS**:
- Resource-hub maintenance: template updates, resource generation, and UI maintenance.
- First-build automation: initial scaffold and first content seeding.
- Website maintenance: promotion to production and ongoing content operations.

**Implementation location**: keep the complete templated editorial ruleset in a clearly labeled section of the site's global stylesheet.

---

### client-cta-href-discipline-subdomain-vs-main-site [PROTECTED, USER DIRECTIVE]


**Cross-references**: `global-css-scope-templated-only-local-handauthored` provides the companion styling rule. Verify CTA destinations on the preview deployment before promotion to production.

**The rule (CRITICAL)**: when a resource hub or other subdomain site has CTAs targeting main-site pages, such as contact, pricing, showroom visits, or careers, the href MUST be the ABSOLUTE URL on the main site, NEVER a relative path that does not exist on the current subdomain.

**The failure mode this prevents**: a shared call-to-action component defaults its link to a relative `/contact`. On a kitchen-equipment library served from `guides.hearthpan.example`, there is no `/contact` route; the form lives at `https://www.hearthpan.example/contact/`. Every page using the component then displays a CTA that returns 404. The hub's build can still succeed, leaving visitors to discover the failure after deployment.

**Per-site URL discipline**: record `main_site_base_url` during initial requirements gathering, for example `https://www.hearthpan.example/`. Shared CTA components and per-pattern templates derive contact destinations from that base URL and the verified contact route. Record other destinations, such as pricing or showroom visits, as needed for the site.

**Generator contract**: when emitting a CTA targeting a path that does not exist on the current site, use the ABSOLUTE URL of its verified destination. If the link opens in a new tab, include `target="_blank" rel="noopener noreferrer"`.

**Reflector check**: verify that all CTA hrefs in generator output are either (a) on-site relative paths to routes that EXIST on this site, or (b) absolute URLs to known-good destinations. Flag REFINE for any href that appears to target a main-site page but is relative.

**Pre-production check**: audit the generated HTML before merging to the production branch. Run this command from the generated-output directory:
```bash
rg --no-heading --no-filename --only-matching 'href="/[^"]*"' . | sort -u
```
Every relative href must resolve to an actual route served by the site. Check runtime routes as well as static output. This catches broken-link regressions before visitors encounter them.

**Known canonical CTA destinations**: record these per site at first-build time. For an invented kitchen-equipment maker: Contact → `https://www.hearthpan.example/contact/` | Privacy → `https://www.hearthpan.example/privacy/` | Main site → `https://www.hearthpan.example/` | Resource library → `https://guides.hearthpan.example/`.

**Forward-applicable to every site and every automation that writes CTAs**, including resource-hub maintenance, first builds, website maintenance, content generation, and content review. Subdomain sites must use absolute URLs for main-site routes.

---
## Page-Pattern Corrections

Bundle of reusable corrections to resource-page patterns. Apply them to both the page templates and existing pages. Pattern numbers follow `03_skills/resource-hub-resource-page-builder/SKILL.md`: Pattern 3 is a locally hosted, file-bearing resource page; Pattern 4 is an independent review or external feature (including an externally hosted customer story) that lives on another site and is summarised here. A page whose stored HTML owns its own layout is a separate concept, called Pattern S below.

### `customer-story-descriptor-bullets-only-001` [PROTECTED: Pattern 4 external feature]

- **Purpose**: Help readers assess a resource without reading a long introduction that repeats it.
- **Rule**: The Pattern 4 descriptor, including any summary block, renders as bullet points only. Use 4-8 short bullets, each a single declarative sentence or fragment. No paragraph prose.
- **Supersedes**: Paragraph descriptors in earlier versions of the template.

### `customer-story-summary-header-rename-001` [Pattern 4 external feature]

- **Purpose**: Give the summary a short, direct label.
- **Rule**: Use the single word "Summary" as the summary section heading on every Pattern 4 page, so readers recognise it across the hub.
- **Supersedes**: Longer explanatory summary labels in earlier versions of the template.

### `customer-story-summary-below-key-outcomes-001` [Pattern 4 external feature]

- **Purpose**: Present the useful outcomes before the supporting context.
- **Rule**: On a Pattern 4 page, put the customer's **key results** before the **Summary**, in the words the customer approved. Near the top, credit the customer by the name and role they approved, and add a visible link to the original story if one exists. The remaining content follows the Pattern 4 list in `03_skills/resource-hub-resource-page-builder/SKILL.md`. Results tell a skimming reader what changed for the customer; the summary then gives context.
- **Supersedes**: Earlier template ordering that placed the summary before the outcomes.

### `no-bottom-cta-box-on-pages-001` [PROTECTED: UNIVERSAL across all page patterns]

- **Purpose**: Keep resource pages focused on helping readers learn.
- **Rule**: Remove the bottom-page sales CTA section, panel, or banner between the content and the "Back to all resources" link on EVERY resource detail page.
- **Supersedes**: Any persistent sales CTA at the end of a resource-page template.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Strip existing bottom sales CTAs during the next maintenance pass.

### `no-breadcrumbs-on-resource-pages-001` [PROTECTED: UNIVERSAL]

- **Purpose**: Keep the resource header simple and focused.
- **Rule**: Remove the visible breadcrumb trail at the top of every resource detail page. The page header starts directly with H1. Accurate BreadcrumbList JSON-LD may remain in the structured data.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Strip existing visible breadcrumbs during the next maintenance pass.

### `no-all-caps-metadata-strip-001` [PROTECTED: UNIVERSAL]

- **Purpose**: Reduce visual clutter below the title.
- **Rule**: Remove the all-caps metadata strip below the page title, including resource type, topic, products, file format, file size, and page count. The hero contains H1 only. Keep metadata in Sanity without displaying that strip.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Strip existing metadata strips during the next maintenance pass.

### `no-related-resources-tagline-001` [PROTECTED: UNIVERSAL]

- **Purpose**: Let the related-resource cards explain their own relevance.
- **Rule**: Remove the explanatory tagline under the related-resources heading. The section contains a heading and a grid of 2-4 cards, with no tagline between them.
- **Supersedes**: Explanatory taglines in earlier templates; the rest of the section remains unchanged.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Strip existing taglines during the next maintenance pass.

### `related-resources-header-rename-001` [UNIVERSAL]

- **Purpose**: Use one consistent label for resource recommendations.
- **Rule**: Change "Similar resources" to "Related resources" verbatim across every page pattern.
- **Supersedes**: The earlier heading label; the rest of the section remains unchanged.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Rename existing section headings during the next maintenance pass.

### `no-whats-inside-header-merge-into-descriptor-001` [PROTECTED: UNIVERSAL, guide/spec-sheet/file-bearing patterns]

- **Purpose**: Avoid repeating the resource description in a second section.
- **Rule**: Remove the "What's inside" heading and body from guide and spec-sheet pages. Merge useful content into the top descriptor using the bullet format. The descriptor already explains what the resource contains.
- **Applies to**: Pattern 3 guides, spec sheets, and future file-bearing patterns.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Merge the useful content into the descriptor and delete the redundant section during the next maintenance pass.

### `file-preview-before-download-001` [PROTECTED: UNIVERSAL, file-bearing patterns]

- **Purpose**: Let readers inspect a file before deciding to download it.
- **Rule**: On every file-bearing page, place the file PREVIEW block FIRST in the visual flow and the DOWNLOAD button BELOW it.
- **Applies to**: Pattern 3 guides, spec sheets, and future file-bearing patterns. Pattern 4 pages link to the original host instead of hosting a local copy.
- **Propagation**: Apply to both first builds and ongoing maintenance.
- **Retroactive**: Reorder existing file pages to show the preview before the download during the next maintenance pass.

---

## Customer-Story Ingest Rule

### `customer-story-ingest-verification-and-url-rule-001` [PROTECTED: UNIVERSAL]

For every customer story added to a resource hub, ALL of these checks must pass or the story is EXCLUDED:

**Check 1, Customer approval**: The customer has agreed in writing (an email reply is enough) to have the story published on this site, and the approval says what may be used: their name, logo, photos and quoted words. Keep the approval with the site's own records, never on the page. For an invented kitchen-equipment maker, a bakery owner who agreed to a story about baking with its countertop mixer reads and approves the draft page before it goes live.

**Check 2, Approved words only**: Quote only what the customer approved, word for word. Do not polish a quote, join two quotes into one, or add a result the customer did not state. If the page needs different wording, send it back to the customer for approval first.

**Check 3, Credit and link**: Credit the customer by the name and role they approved. If the story was first published somewhere else, such as the customer's own blog or a local newspaper, the `externalUrl` field links to that original, and the link must open the story itself, not a listing page or a home page. If no original exists, leave `externalUrl` empty and let the page on your hub be the story.

**Validation procedure**: Before publishing, compare every quote and every named detail on the page with the approved text. If there is an original link, follow its redirects and confirm it opens the story. Record who approved the story and when beside the resource document, in a field such as `customerApproval`.

**Retroactive**: Flag any existing customer story with no recorded approval for removal or re-approval during the next maintenance pass.

Apply the same checks during initial ingestion and later reviews.

### workflow-l-one-agent-per-page-canonical-NO-BATCHING [PROTECTED, USER DIRECTIVE]

**THE RULE (PROTECTED)**: Resource-page generation MUST dispatch ONE design-generator agent PER RESOURCE PAGE and ONE design-reflector agent PER RESOURCE PAGE. Never batch multiple pages into one generator or one reflector agent.

**Why batching fails**:

1. **Attention dilution → quality drift**: An agent processing several pages spreads its context across them. A per-page agent can focus on one page's source, structure, and validation.
2. **Stream-idle timeouts**: Large batches can time out before all pages are complete. Smaller per-page tasks limit the work exposed to an interruption.
3. **Recovery cost**: After a batched agent times out, each page must be inventoried before unfinished work can be dispatched again.
4. **Atomic clarity**: Per-page logs, validation, and handoffs to reflectors keep evidence attached to the correct page.

**Canonical cadence**: N pages → N generators in bounded parallel groups → N reflectors, each starting as soon as its page is ready → 1 final cross-page reflector checking slug uniqueness, links between pages, and hub behavior.

**ONE EXCEPTION (requires the site owner's explicit sign-off for that run)**: One reflector per pattern is valid ONLY when every affected page has already received an individual review. This can support a shared-template review after page-level checks; it does not replace the initial individual reviews.

**Pre-dispatch orchestrator check**: The dispatch list must contain N individual-page invocations, never batched-page invocations. Flag any orchestration draft that batches pages.

**Forward-applicable**: Resource-hub maintenance, multi-page first builds, template-aware UI updates, content generation, and content review.

## Universal META-PRINCIPLES (cross-automation skills)

| Skill | Status | Purpose |
|-------|--------|---------|
| `memory-source-file-self-containment-001` | PROTECTED UNIVERSAL | When a memory references a file path as its source of truth, the memory body MUST include the verbatim source content needed to understand and apply the lesson. A stored memory may outlive the file it references. |
| `automation-aggressive-memory-storage-discipline-001` | PROTECTED UNIVERSAL | Every run stores frequent, detailed memories (or notes) throughout the work, including current run state and candidate fixes for recurring failures. Do not wait until the end of the run to preserve context. |

Both skills apply universally across all automations.

---

### filter-sidebar-hide-when-zero-unified-canonical [PROTECTED, USER DIRECTIVE]

**The rule**: When a filter sidebar option's count drops to 0 AND the option is not currently checked, HIDE it entirely via `display: none`, using the `.filter-item--empty` or `.filter-option--empty` class. Do NOT fade it with opacity.

**Canonical pattern** for the filter sidebar and resource listing:

```js
opt.classList.toggle('filter-option--empty', n === 0 && !isChecked);
opt.classList.remove('filter-option--dimmed');
```

Use one hide-when-zero behavior, whether filters are untouched or already active.

**Always-visible-when-checked invariant**: A checked option never hides, even if its count is 0. Users must always be able to uncheck their own selections.

**Why HIDE beats DIM**: Empty options get out of the way and reduce cognitive load. Faded options create uncertainty about clickability and occupy sidebar space without offering results.

**Forward-applicable to every hub** with a filter sidebar.

---

### source-grounding-mandatory-for-all-resource-page-generators-001 [PROTECTED UNIVERSAL, USER DIRECTIVE]

**The rule (NON-NEGOTIABLE)**: Every resource-page generator agent MUST fetch source material BEFORE writing any user-facing content, including summaries, bullets, and "Why it matters" sections. NEVER rely solely on prior `htmlContent`. That is second-hand material and accumulates fidelity drift.

**Source fetch paths**:

- **External features and customer stories (Pattern 4)**: Fetch the original from the URL stored in `externalUrl` when one exists. For a customer story, also read the customer-approved text and quote only from it (see the customer-story ingest rule above). If neither the original nor the approved text is available, pause the content rewrite.
- **Internal file-bearing resources (Pattern 3)**: Read the text extraction of the source PDF, such as a bicycle-parts installation guide, a garden-supply how-to article, or a ceramic studio's care guide.

**Generator prompt mandate**: Every prompt MUST include:

1. FIRST fetch the source material or read the source PDF extraction.
2. THEN read current `htmlContent` for STYLE and STRUCTURE only.
3. THEN read the applicable page template for canonical section order and voice.
4. THEN write the summary, bullets, and explanation of relevance grounded in the source.

**Why**: A summary written from a prior page or from memory is second-hand and drifts further from the source with every cycle. Fresh access to the resource itself provides a stable baseline.

**Verification by orchestrator**: Before launching generators, confirm that the prompt template includes the source-fetch step. If a generator's run shows no source-fetch or source-read operation, REGENERATE with the source available.

**Cross-refs**: `customer-story-ingest-verification-and-url-rule-001` for customer approval, approved-quote and original-link checks.

**EXTENSION**: This rule applies to **UPDATES**, not just first builds. Any maintenance run in which a generator touches user-facing words, including a full rewrite, partial section update, style refresh affecting body text, bullet reduction, or section reorder, MUST source-ground first. **No exemption for "this is just an update"**. Fidelity drift accumulates across maintenance cycles.

**Orchestrator enforcement**: Before launching ANY generator during ANY first-build or maintenance run, verify that the prompt template contains the source-fetch step. If it is missing, STOP and update the prompt before launching.

---
### resource-hub-isHidden-reversible-removal-canonical [PROTECTED, USER DIRECTIVE]

**The pattern**: to remove a resource from hub listings without hard-deleting the Sanity document:
1. Set the boolean `isHidden: true` on the resource document with a single Sanity patch.
2. Filter `!defined(isHidden) || isHidden != true` in all hub-facing GROQ queries.

**4 queries to update in the site's Sanity query module**:
- `getAllResources`: library grid
- `getSpotlightResource`: homepage hero binding
- `getRelatedResources`: taxonomy-matched candidates branch
- `getRelatedResources`: fallback recent-picks branch

**Why isHidden beats hard-delete**: It is reversible: flip the flag back and redeploy static pages to restore visibility. It preserves content, schemas, and assets. It also keeps imports idempotent by avoiding a missing-document cycle that recreates deleted records.

**Sister pattern, spotlight swap**: An atomic three-document transaction prevents an intermediate state with no spotlight.
```javascript
const tx = client.transaction();
tx.patch(oldSpotlightId, p => p.set({ isHidden: true, spotlight: false }));
tx.patch(newSpotlightId, p => p.set({ spotlight: true, featured: false }));
tx.patch(newFeaturedId, p => p.set({ featured: true }));
await tx.commit();
```

**Verification**: After building, search the generated listing HTML for the hidden resource's slug. The match count must be zero. After deployment, confirm the same behavior on the live listings. The direct resource URL should still work. Hiding a listing is not access control.

**Applicable to every resource hub**. Seed new documents with `isHidden: false`, include visibility changes in maintenance procedures, and verify that generated listings contain no references to hidden resources.

---

### spotlight-rotation-dual-image-field-binding [PROTECTED, USER DIRECTIVE]

**THE RULE (CRITICAL)**: In this pattern, the spotlight card renders through `hubConfig.heroImage` / `hubConfig.spotlightImage`, stored on the hub configuration document with a 1:1 aspect ratio. Resource cards render through `resource.featuredImage`, stored on each resource document with a 16:9 or 16:10 aspect ratio. These are two separate Sanity surfaces. When rotating the spotlight, check both and patch each that needs a new image.

| Surface | Sanity field | Aspect | Renders |
|---|---|---|---|
| **Spotlight CARD** | Hub configuration: `spotlightImage` + `heroImage` | 1:1 (1024×1024) | Homepage hero only |
| **All Resources CARD** | `resource.featuredImage` | 16:9 or 16:10 (1200×750 for 16:10) | All Resources + Featured grid + Related Resources |

**Anti-pattern**: Assigning a square spotlight image to `resource.featuredImage` crops the square composition into a wide resource-card slot and does not update the spotlight card, which reads from the hub configuration. Symptom: “All Resources changed, but the spotlight didn't.”

**6-Step Spotlight Rotation Runbook**:
1. Apply atomic resource-document patches: flip spotlight flags, optionally set `isHidden`, and adjust featured selections.
2. **Patch the hub configuration's spotlight image fields.** This is the most easily missed step.
3. Keep the resource's existing wide `featuredImage`, or generate one if missing. Never overwrite it with the square spotlight image.
4. Build and search the output to verify that the new square image appears, the wide resource image appears, and the retired image is absent from the placements being replaced.
5. Update the CTA label if the spotlight rotates between resource types. Rebuild if this changes generated output.
6. Commit and push through the site's release process.

**Applicable to every spotlight rotation**. Include separate hub and resource image fields in the initial Sanity schema, document the rotation procedure, and verify image bindings before production promotion.

## Above-the-Fold Media Governance + Collaborative Editing

### media-001: Above-the-Fold Media Governance [PROTECTED]
**Rule**: Any element competing for the LCP slot follows a shared review discipline, regardless of asset class: image, video, WebGL, WebGPU, or a future format. Apply class-specific byte budgets, encoding conventions, and checks before deployment.

**Weight Budgets**:
- Images: ≤500KB AVIF/WebP, ≤300KB poster; prefer AVIF, then WebP, then JPEG where appropriate. Use quality 75–82 for content and 85 for hero imagery as starting points; avoid lossless exports for photographic assets.
- Video: ≤20MB for a 1080p hero up to 30s, preferably ≤10MB; H.264 high profile level 4.0, yuv420p, CRF 23, slow preset, faststart required, audio stripped.
- WebGL canvas + bundled JS: ≤200KB bundle for Three.js scenes, ≤50KB for canvas controllers; opacity 0.5–0.6 for ambient backgrounds; `pointer-events: none` unless interactive.
- Future asset classes: review delivery, accessibility, and rendering costs before adding a new convention; apply the same rubric.

**LCP Discipline**:
- For images that are the LCP candidate: `loading="eager" fetchpriority="high" decoding="async"` plus explicit width and height. See qa-016.
- For video, prioritize the poster as the intended initial paint. Video frames can also affect LCP, so measure the actual candidate. Use `preload="metadata"` or `preload="none"` to limit early video loading. Where supported, a `<source media="(min-width:768px)">` pattern can select desktop video while mobile receives the poster; verify actual requests and rendering.

**Master vs Web Export Topology**:
- Master files, including designer handoffs and raw or editing codecs such as APV, ProRes, and DNxHD, belong in a separate asset store outside the website repository.
- Commit web exports to the site's public asset directory.
- Re-encode at handoff time with FFmpeg or a compatible PyAV build.
- The decoder fallback procedure appears in media-002.

**Pre-Deploy Gate**:
Set `BUILD_DIR` to the generated site directory before running these checks:
```bash
find "$BUILD_DIR" -type f -name '*.mp4' -size +20M
find "$BUILD_DIR" -type f \( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \) -size +500k
find "$BUILD_DIR" -type f -name '*.js' -size +200k
du -sh "$BUILD_DIR"
```
- Video matches fail the check unless there is a documented, reviewed exception.
- Raster-image matches trigger review; check AVIF, WebP, and posters against their budgets too.
- JavaScript matches trigger review; identify graphics bundles and apply their class-specific limits.
- Total generated site size: warn at 15MB and fail at 25MB per site.

**Failure mode and fix**: A kitchen-equipment maker's resource library can accidentally ship an editing master as its homepage video. Exporting a delivery codec and compressing the poster reduces transfer weight. Measure before and after with Lighthouse rather than inferring an LCP improvement from file size alone.

**Tags**: above-fold-media-governance, weight-budget, lcp-discipline, asset-class-future-proof
**Status**: active [PROTECTED]

### collab-001: Collaborative Website Build + Edit + Maintenance Discipline [PROTECTED]
**Rule**: Every website may have multiple contributors, including parallel editing sessions. Check remote changes before editing, review asset sizes before committing, and keep development separate from production to prevent overwrites, divergence, and silent regressions.

**Pre-Edit Ritual** (every session, every contributor):
1. Change into the website repository.
2. Run `git fetch origin` to update the configured remote-tracking refs.
3. Run `git status` and resolve or preserve existing work before proceeding.
4. Run `git rev-list --left-right --count origin/preview...preview` to compare the local and remote development branch.
5. If `origin/preview` is ahead and the working tree is ready, run `git pull --rebase origin preview`. If both sides have commits, inspect the divergence and resolve it deliberately.
6. When another contributor is editing, also run `git log origin/preview --since=24hr --oneline` and read those commits before pushing.

**Branch Hygiene** (enforce through repository and hosting settings where supported):
- `main` is production-only; changes reach it through the reviewed release process.
- `preview` is the shared active-development branch for substantive work.
- Never push directly to `main` outside that release process.

**Pre-Commit Asset-Size Gate**:
- Any file >5MB outside designated video, WebGL, or 3D asset directories requires manual review before committing.
- Designated heavy-asset directories still follow media-001 budgets.

**Storage Topology**:
- Masters belong in an asset store outside the repository and remain the source of truth.
- Web exports belong in the website's public asset directory and are committed.
- Keep a per-site record mapping each master to its web exports.

**Tags**: collaborative-website-build, pre-edit-ritual, pre-commit-asset-gate, branch-hygiene, master-vs-export-topology
**Status**: active [PROTECTED]

### media-002: PyAV Decoder Fallback Recipe
**Rule**: When FFmpeg reports “unknown codec” or “Decoder not found” for a master video, inspect the source codec and the installed build's decoder support. A newer compatible PyAV/FFmpeg build may provide the required decoder, but a version number alone does not guarantee support. If no available decoder supports the source, request an interoperable export.

**Recipe**: Open the source with `av.open(src)`, demux and decode, reformat frames to `yuv420p`, and encode with `add_stream("libx264")` using `{"crf": "23", "preset": "slow", "profile": "high"}`. Apply `{"movflags": "+faststart"}` to the output MP4 container. Preserve frame timing, flush the encoder, and omit audio for decorative hero video.

### media-003: Lighthouse Control vs Treatment Discipline
**Rule**: Before making a performance-impacting change, such as an asset swap, library upgrade, or layout adjustment, capture a baseline Lighthouse run. Compare control and treatment after the change under matching conditions.

**Pattern**: Set `PAGE_URL` to the page under test and `CONTROL_REPORT` and `TREATMENT_REPORT` to separate JSON output locations.
```bash
npx lighthouse "$PAGE_URL" --only-categories=performance --form-factor=mobile --output=json --output-path="$CONTROL_REPORT" --chrome-flags="--headless=new --no-sandbox"
```
Make the change, then repeat:
```bash
npx lighthouse "$PAGE_URL" --only-categories=performance --form-factor=mobile --output=json --output-path="$TREATMENT_REPORT" --chrome-flags="--headless=new --no-sandbox"
```
Compare Performance score, LCP, and total bytes. Keep browser, throttling, cache conditions, and test environment consistent; repeat runs when variation could explain the result.

**Why**: Without a control measurement, you cannot substantiate improvement. You can only report the measured end state.

---

## Curator Log: Above-the-Fold Media Governance

| Context | Trigger | Action | Skills |
|------|---------|--------|--------|
| Bicycle-parts guide library | An editing master is used as a homepage hero video. | Keep masters outside the repository, produce a web export, enforce asset budgets, and compare Lighthouse measurements before and after the change. | media-001, collab-001, media-002, media-003 |
| Garden-supply how-to hub | Decorative banner imagery competes with overlay text and leaves a visible seam against the section background. | Blend decorative imagery with the section color, match image-edge colors to the CSS background, and use a radial backdrop where additional text separation is needed. | pil-softening-pattern-text-overlay-001, banner-css-replication-mandate-001, radial-backdrop-pattern-for-text-on-banner-001 |

### pil-softening-pattern-text-overlay-001
**Rule**: When generating decorative banners for sections with text overlays, such as customer quotes or selected spotlight sections, generate a full-presence original, then create a softened companion with PIL: `Image.blend(solid_bg_pil, banner_pil, alpha=0.65)`. Match the solid background color to the section's CSS background exactly. Use the softened image in production and retain the original in the asset store.

**DO NOT soften**: Heroes whose gradients provide the intended fade, spotlight banners whose imagery supplies the full atmospheric setting, or product banners where subject detail is essential.

**DO soften**: Decorative quote banners, customer-story section banners, and compositions with an open text area where imagery provides supporting texture.

**Why**: On an invented ceramic studio's customer-story banner, blending can keep the artwork visible without overwhelming the quote. Treat alpha 0.65 as a starting point, not a universal result. Lower values reduce image presence; higher values preserve more detail and may compete with text. Verify contrast and readability at the actual display size.

**How to apply**: After image generation, branch by banner purpose. For decorative text-overlay banners, use `Image.open`, `Image.new` with the section background color, and `Image.blend`. Export a clearly labeled softened version as the production asset. Add a radial text backdrop if needed, and verify text contrast over the finished composition.

### banner-css-replication-mandate-001
**Rule**: Every banner background must match the section's CSS background at the edges where they meet. For solid backgrounds, use the exact hex value. For gradients, reproduce the direction, color stops, transparency, and displayed alignment. A mismatch between an image layer and the underlying CSS background creates a visible seam.

**Why**: An invented regional bakery chain might use `#EDF2E8` for a pale section background. A banner with a slightly different edge color can expose a visible 1–2px band where the image meets the section. Include the exact color in the generation prompt, then inspect and correct the exported edge pixels if necessary. Prompt wording alone does not ensure an exact match.

**How to apply**: Include the section's CSS background hex in image-generation prompts. For gradients, specify the direction and each color stop. Place the exported image over the actual section background in browser developer tools and inspect the edges at desktop and mobile sizes. Adjust the asset or composition until the transition is seamless.
### radial-backdrop-pattern-for-text-on-banner-001 [CROSS-REF with site builds]
**Rule**: For any text that sits over a banner image (a pull quote, a section intro, a featured-resource caption), apply a radial-gradient backdrop on the text element for legibility WITHOUT visible box edges.

**CSS pattern**:
```css
.text-overlay-element {
  --backdrop-rgb: 255, 255, 255;
  padding: clamp(24px, 3vw, 40px) clamp(40px, 4vw, 56px);
  background: radial-gradient(ellipse 110% 100% at center,
    rgba(var(--backdrop-rgb), 0.78) 0%,
    rgba(var(--backdrop-rgb), 0.52) 55%,
    rgba(var(--backdrop-rgb), 0) 95%);
  border-radius: 24px;
}
```

Dark background sections: set `--backdrop-rgb` to the background's dark RGB values. Light background sections: use `255, 255, 255`. Ellipse size 110% 100% gives a soft halo; 130% 110% gives a broader falloff.

**Why**: A solid white box behind banner text reads as a card and breaks the editorial feel. Heavy text shadows can distract from the content. A radial backdrop that reaches 0% alpha at its edges softens the image behind the text without creating a visible boundary. This suits image-led sections in a kitchen-equipment maker's resource library.

**How to apply**: During CSS integration, add the radial-backdrop class to text-on-banner sections. Tune opacity to the banner's brightness and verify text contrast. Don't use border-radius > 24px, which can make a visible backdrop read as a pill.


---

## Curator Log: Pattern S Three-Layer Fidelity Contract

| Context | Trigger | Action | Skills |
|---------|---------|--------|--------|
| Template integration | A bicycle-parts guide matched its standalone preview but lost styling and navigation behavior in Astro. An earlier template had embedded styles inside htmlContent, hiding missing support for separate fields. The new template used htmlStyles, which was omitted from the Sanity query and the Astro page output. Its embedded scroll-spy script also failed to initialize through the HTML injection path. | Document the three-layer contract and supporting checks: complete query projections, page-level style and schema injection, Astro script initialization, frontmatter string assembly, local builds, deployment-log diagnosis, stable preview URLs, deployed-page tests, scroll-spy behavior, and visual comparison. Apply the same checks to initial builds and maintenance. | pattern4-three-layer-fidelity-contract-canonical-001 and the companion skills below |

### pattern4-three-layer-fidelity-contract-canonical-001 [PROTECTED, UNIVERSAL: applies to builds and maintenance]

**Rule**: Three layers must ALL be wired before a Sanity Pattern S resource renders with template fidelity. Pattern S (self-styled HTML page) means a resource whose stored HTML owns its inner page layout, with companion fields for styles and structured data. It is not one of the numbered content patterns in the resource-page builder skill; any of them can be stored this way. (The skill ID keeps its older `pattern4` name so existing citations still resolve.)

1. **LAYER 1, Sanity GROQ projection**: Every query that fetches `resource` documents for a resource detail page MUST project `htmlContent, htmlStyles, htmlSchemas` together. Check both the query used by `getStaticPaths` and the query used at render time.
2. **LAYER 2, Astro page injection**: The branch that renders the stored layout MUST inject `resource.htmlStyles` in a `<style data-resource-styles="..."></style>` element AND `resource.htmlSchemas` in a `<script type="application/ld+json">`. Prefix CSS selectors with the resource wrapper to scope the styles; the data attribute alone does not scope them. Hoist assembled markup into frontmatter constants (`const htmlStylesBlock = resource.htmlStyles ? ... : ''`) and render as `{htmlStylesBlock && <Fragment set:html={htmlStylesBlock} />}`. This keeps nested string construction out of JSX.
3. **LAYER 3, Script execution**: Do not rely on scripts embedded INSIDE `htmlContent` to initialize interactive behavior. Scripts inserted through `innerHTML` are inert, and execution can differ between initial document parsing and later DOM updates. Put scroll-spy, accordion, and modal initialization in a top-level Astro `<script>` block, gated on a wrapper-class detector so it does nothing on unrelated pages.

**Why**: A standalone preview can look correct while the Astro render has no resource styles and an inactive table of contents. Templates with styles embedded inside `htmlContent` can hide missing support for the separate style field until another template uses it.

**How to apply**: When converting ANY prepared HTML template to a Sanity-backed Astro resource page, check all three layers. After the preview deployment is ready, run the deployed-page checks in `ace-reflector-production-test-gate-live-render-mandatory-001`.


### sanity-query-htmlstyles-htmlschemas-projection-canonical-001 [PROTECTED]

**Rule**: Every GROQ query that fetches `resource` documents for Pattern S rendering MUST project `htmlContent, htmlStyles, htmlSchemas` together. Check queries for all resources, a resource by slug, series resources, and related resources whenever they carry `htmlContent`.

**Why**: Scaffolds may project only `htmlContent`. Forgetting the companion fields silently drops styles and schemas at the data-fetch layer. The field exists in Sanity and appears in the editor, but the page never receives it.

**Verification**: After editing, run `npx astro build` and inspect the generated resource HTML for `data-resource-styles` AND `application/ld+json`. Both must appear when the source resource supplies them. For server-rendered routes, inspect the served response as well.


### astro-set-html-script-inert-gotcha-canonical-001 [PROTECTED, UNIVERSAL]

**Rule**: Scripts inserted with `innerHTML` do not execute. Astro's `set:html` renders HTML, but it is not a reliable lifecycle mechanism for scripts stored in Sanity content, particularly when that content is inserted or replaced on the client. Move interactive initialization to a top-level Astro `<script>` block, gated on a wrapper-class detector. Inside an initialization function, use `if (!document.querySelector('.resource-guide')) return;` so shared page code does not run unnecessarily.

**Why**: A garden-supply how-to article's scroll-spy may work in a standalone document and fail when the same markup reaches the page through a different insertion path. Page-level initialization makes the behavior explicit and testable.


### jsx-nested-template-literal-esbuild-trap-canonical-001 [UNIVERSAL]

**Rule**: Complex template literals written directly inside JSX attributes are easy to break with mismatched backticks, braces, or interpolation boundaries. For markup such as `<Fragment set:html={htmlStylesBlock} />`, assemble the string in a frontmatter constant first, then reference the bare identifier: `{htmlStylesBlock && <Fragment set:html={htmlStylesBlock} />}`. If esbuild reports `Unexpected "}"`, inspect the surrounding source delimiters and JSX comments. Backticks or `${}` inside a runtime string value do not themselves cause a parse error. Also check for stray `}` after JSX comment closures introduced by incomplete edits.


### ace-reflector-production-test-gate-live-render-mandatory-001 [PROTECTED, UNIVERSAL: Reflector dim 6 hard gate]

**Rule**: The ACE Reflector's dimension 6, “AEO + deployed-page verification,” MUST require evidence from the LIVE DEPLOYED URL, not just the self-contained preview. Use Playwright against the deployed preview or production URL and assert:

1. The expected wrapper class exists in the DOM.
2. `style[data-resource-styles]` exists with `.textContent.length > 1000` for templates whose expected stylesheet exceeds that lower bound. Set an appropriate bound for smaller templates.
3. The `script[type="application/ld+json"]` count matches the expected count.
4. A computed style on a signature element matches its design token, such as a feature heading's font weight or a banner's background gradient.
5. Sanity CDN images resolve with `naturalWidth > 0`.
6. Interactive behavior works: scroll to a known H2 offset and verify that the matching table-of-contents link gains `.is-active`.
7. At the 375px mobile breakpoint, the layout stacks correctly, including `order: -1` for a figure intended to move first and `position: static` for the sidebar.

**Verdict**: Any failed assertion means CONTINUE. All passing permits SATISFACTORY, with composite ≥ 9.8 still required across all 7 dimensions.

**Why**: A ceramic studio's guide can pass visual review as a standalone preview while its deployed page has no resource styles. Testing the deployed page catches failures introduced by data fetching, rendering, and hosting.


### template-to-astro-build-fidelity-verification-recipe-001 [PROTECTED]

**Rule**: Run this baseline check and seven-step recipe on EVERY new template-to-Sanity-to-Astro conversion.

0. Verify the self-contained preview at 1440px, 1280px, and 375px.
1. Remove supplied header, footer, related-resource, and breadcrumb markup wherever Astro owns those elements. Separate the template into HTML body content, CSS, and structured-data JSON.
2. Upload images to Sanity, substitute the resulting URLs, and submit a `createOrReplace` mutation through the dataset's mutation API.
3. Check the three-layer contract: query projection, Astro page injection, and Astro-level initialization for interactivity.
4. Run `npx astro build` locally. Inspect generated output for `data-resource-styles`, `application/ld+json`, and the wrapper class. Check a served response when the route uses server rendering.
5. Push to the preview branch, wait for the Vercel deployment to become ready, and run the seven deployed-page assertions above.
6. Compare the deployed page visually with the baseline at all three viewports.
7. Review the preview URL with the site maintainer, then change the resource from Draft to Published and merge to the production branch.


### scroll-spy-astro-script-canonical-001 [REUSABLE ACROSS SITES]

**Rule**: Use a reusable Astro `<script>` block for article templates with a sticky table-of-contents sidebar. Detect a wrapper such as `.resource-guide` and return from initialization when it is absent. Query `h2[id]` in `.article-body`, index `.toc a[href^="#"]` by fragment, and use IntersectionObserver with `rootMargin: '-15% 0px -55% 0px'` to toggle `.is-active` on the matching link. Provide a scroll-listener fallback for browsers without IntersectionObserver. To reuse it on a regional bakery chain's guide hub, change the wrapper selector and tune the active-state CSS to the site's accent color. The navigation logic stays the same.


### astro-check-vs-astro-build-divergence-vercel-deploys-on-build-only-001

**Rule**: `astro build` catches build and parse failures but does not perform full TypeScript checking. `astro check` checks Astro and TypeScript diagnostics. A deployment configured to run only `astro build` can therefore succeed despite type errors. Type-check errors block deployment only when the configured build process includes that check.

**How to apply**: BEFORE pushing a resource detail-page edit to preview, run `npx astro build` locally to catch parse failures before a remote build cycle. Run `npx astro check` as well to catch type errors, and include it in deployment checks when type safety is required.


## Curator Log: AEO Blog Batch on a resource hub

| Context | Trigger | Action | Skills Added |
|---------|---------|--------|--------------|
| Batch review | A kitchen-equipment resource-library batch exposed recurring defects: visual cues that became ambiguous between columns, literal HTML placeholders in content patches, and cross-article links guessed from working-directory names. Reviews after each batch caught these before ingestion and carried the fixes into later work. Final acceptance required the 9.80 threshold without rounding. | Consolidate lessons on template fidelity, deployment checks, content-query completeness, source verification, image preparation, generator discipline, and fair comparisons. Carry reusable corrections into both build and maintenance guidance. | Canonical rules and supporting review practices below |

**5 most load-bearing canonicals from batch review**:

1. `pattern4-three-layer-fidelity-contract-canonical-001`: verify data fetching, rendering, and interactive initialization together.
2. Derive figure requirements from the source content, then verify that every required image is present.
3. `generator-sanity-patch-content-embed-via-json-dumps-canonical-001`: serialize real HTML and verify it after reading the patch back.
4. `blog-fair-incumbent-voice-canonical-when-naming-competitor-001`: describe named alternatives fairly and ground comparisons in evidence.
5. Search generated content for unresolved placeholders and disallowed structural shortcuts before publication, then inspect each match in context.

### Generator Discipline Cluster

#### generator-sanity-patch-content-embed-via-json-dumps-canonical-001 [PROTECTED-graduation queue, UNIVERSAL]
**Rule**: Generators that produce Sanity content patches MUST serialize actual HTML with `json.dumps`, never substitute a placeholder such as `"htmlContent": "{{HTML_CONTENT}}"` for the content. Build a Python dictionary containing the real `html_string`, then serialize the complete dictionary. Round-trip verification: after writing the patch, immediately read it with `json.load` and assert `len(parsed["htmlContent"]) > 1000`, or the expected lower bound for that resource. Also check that no unresolved placeholder remains.

**Why**: A patch containing a literal placeholder can be valid JSON and still publish broken content. Serializing the real HTML preserves escaping, while reading it back and checking its contents catches incomplete generation before ingestion.
#### generator-cross-blog-slug-via-sibling-sanity-patch-not-directory-name-canonical-001 [UNIVERSAL]
**Rule**: When a blog Generator references a sibling blog's URL, for example in a cross-blog link or related-resource block, the slug MUST come from the sibling's Sanity patch payload `.slug.current` field, NEVER from workspace directory names. Workspace directories are author-chosen and not authoritative; the sibling's patch defines the intended published slug.
**Why**: Reconstructing slugs from directory names can reverse or otherwise alter their words, producing broken links. Before ingest, assert that every cross-blog slug reference matches the sibling's `.slug.current`; for already published content, also verify the live destination.

#### blog-fair-incumbent-voice-canonical-when-naming-competitor-001 [PROTECTED, UNIVERSAL]
**Rule**: When a blog names a competitor or incumbent solution, acknowledge its legitimate strengths BEFORE pivoting to differentiation. Never lead with the comparator's weaknesses. Pairs with `S-W4-008`, the Q&A panel pre-emptive concession move.

### Process Discipline Cluster

#### ace-curator-per-wave-mandatory-canonical-001
**Rule**: In multi-wave content batches, run the ACE Curator at the close of EACH wave, not only at batch-end. Each wave's Curator findings feed the next wave's Generator guidance. The last wave's Curator doubles as the batch-final Curator.
**Why**: Passing harmful patterns and helpful skills forward prevents later waves from repeating avoidable mistakes, including broken slug references.

#### blog-figure-open-layout-no-box-canonical-001 (pre-existing, re-confirmed) [PROTECTED, UNIVERSAL]
**Rule**: In-blog figure images sit open in the body with NO box, border, padding, or background, just the image and a centered italic figcaption. Applies to ALL blog templates on the site.

### Vercel/Astro Build Cluster

The following canonicals form a reusable build reference:
- `pattern4-three-layer-fidelity-contract-canonical-001` [PROTECTED, UNIVERSAL]
- `sanity-query-htmlstyles-htmlschemas-projection-canonical-001` [PROTECTED]
- `astro-set-html-script-inert-gotcha-canonical-001` [PROTECTED, UNIVERSAL]
- `jsx-nested-template-literal-esbuild-trap-canonical-001` [UNIVERSAL]
- `ace-reflector-production-test-gate-live-render-mandatory-001` [PROTECTED, UNIVERSAL]
- `template-to-astro-build-fidelity-verification-recipe-001` [PROTECTED]
- `scroll-spy-astro-script-canonical-001` [UNIVERSAL]
- `astro-check-vs-astro-build-divergence-vercel-deploys-on-build-only-001`
- Inspect deployment build logs when diagnosing Vercel failures.
- Use a stable preview branch alias for review links, and verify which deployment it serves.

### Curator-Graduated Wave Skills

#### S-W2-001 comparison-table-fair-visual-treatment-no-advocacy-cue
**Rule**: Comparison tables, whether HTML or another format, MUST render every column with symmetric visual treatment. Do not use asymmetric color, weight, or icons to signal a preferred side. For example, a kitchen-equipment maker comparing countertop mixers should give each option equal visual prominence. Tags: comparison-table, visual-rhetoric, fair-treatment. Status: active

#### S-W2-002 c-cluster-html-comparison-table-render
**Rule**: Criteria-based comparison blogs render comparison tables natively in HTML, not as images. This preserves accessibility, retrieval, and reflow on mobile. Tags: criteria-comparison, html-comparison-table, template-discipline. Status: active

#### S-W2-003 cross-blog-figure-differentiation-explicit-avoid-fence [UNIVERSAL]
**Rule**: Sibling blogs in the same batch must use visually distinct figure compositions. The Generator includes an explicit list of prior blogs' figure motifs to avoid, preventing visual collision. Tags: cross-blog-figure, differentiation, universal. Status: active

#### S-W2-004 rework-angle-entity-dense-discipline
**Rule**: Technical blogs that reframe a published guide for a new audience must retain concrete, source-supported details. For a bicycle-parts company's maintenance guide, these might include component names, compatible mounting standards, required tools, and model-version differences. Reframing must not turn useful instructions into vague advice. Tags: technical-content, rework-angle, entity-density. Status: active

#### S-W3-005 unusual-structure-mapper-ban-grep-verified-pre-publish-canonical-001 [UNIVERSAL]
**Rule**: Before publishing, run a text search across every publish surface, including Sanity patch payloads, HTML, and structured data, for a project-defined rejection list. Invented examples include `TODO_COPY`, `sample-link.invalid`, and temporary `layout-probe-*` class names. Require a per-blog verification table recording each check and result. This catches scaffolding and placeholders that visual review can miss. Tags: pre-publish-search, placeholder-check, universal. Status: active

#### S-W3-006 cross-blog-link-deep-anchor-when-criterion-specific-canonical-001
**Rule**: Cross-blog links that refer to a specific criterion USE a verified section fragment, such as `#drainage-options` in a garden-supply guide. Links referring to the whole article use the bare slug. Tags: cross-blog-link, deep-anchor, criterion-specific. Status: active

#### S-W3-007 featured-does-more-visual-work-for-zero-figure-blogs-canonical-001
**Rule**: When a blog has no in-blog figures, the featured image carries the visual narrative. Require four prompt properties: subject, lighting, composition geometry, and accent palette. Tags: zero-figure, featured-image, prompt-discipline. Status: active

#### S-W4-008 blog-fair-incumbent-voice-q-and-a-preemptive-concession-canonical-001 [UNIVERSAL]
**Rule**: In a Q&A panel, surface the strongest objection and acknowledge its valid premise before pivoting to a substantive difference. For example, a ceramic studio discussing handmade tableware can acknowledge the consistency of factory-made pieces before explaining variations in its own work. Pairs with its PROTECTED parent `blog-fair-incumbent-voice-canonical-when-naming-competitor-001`. Tags: q-and-a-panel, pre-emptive-concession, fair-incumbent, universal. Status: active

#### S-W4-009 blog-operator-as-archetype-persona-voice-third-person-canonical-001 [UNIVERSAL]
**Rule**: In articles using an operator archetype, describe the operator in the third person and reserve every "you" for the decision-maker. A regional bakery chain might describe a fictional shift lead while addressing the store manager directly. Use clearly fictional composites; obtain permission before replacing them with identifiable people, locations, or organizations. Tags: operator-archetype, third-person, persona-voice, universal. Status: active

#### S-W4-010 taxonomy-expansion-for-cross-cluster-retrieval-coverage-canonical-001 [UNIVERSAL]
**Rule**: Add a category outside the article's primary topic when all three conditions hold: (a) the body substantively discusses that use case, (b) a trusted source confirms the use case is real, and (c) the category fits the hub's taxonomy schema. For example, a kitchen-equipment care guide may also belong under storage when it gives supported storage instructions. Tags: taxonomy-expansion, cross-topic, retrieval-coverage, aeo, universal. Status: active

---

## Curator Log: SSR Detail + Prod Rebuild + AEO-Hidden-Listing on a Resource Hub

A form integration and broken production resource links prompted a review of Astro architecture, form integration, deployment discipline, listing visibility, and build diagnosis. The resulting rules apply to CMS-backed resource hubs maintained by one person or a small team.

### Failure mode discovered (the trigger for this review)

**The SSR-listing/SSG-detail mismatch class.** A bicycle-parts guide library displayed newly published cards because its listing used SSR and fresh Sanity reads. Every new card led to a 404 because the detail pages used SSG with `prerender = true` and `getStaticPaths`. Their routes had been baked at the last build, before those guides were published. A successful listing response concealed broken destinations until someone clicked through.

### Architectural-canonical skills added (UNIVERSAL, reusable across sites)

#### S-SSR-001 astro-ssr-listing-ssg-detail-mismatch-failure-mode-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: When a resource listing is SSR and fetches the CMS at request time, but its detail pages are SSG with `prerender = true` and `getStaticPaths`, content published AFTER the last production build can create visible cards without detail routes. Symptom: 200 on the listing, 404 on newly published slugs. Detection: mandatory per-slug curl verification after every production deploy. Fix: convert detail pages to SSR with edge caching, as described in `S-SSR-002`, OR enforce the content-batch production rebuild discipline in `S-SSR-003`. Tags: astro, ssr, ssg, sanity, failure-mode, universal, protected. Status: active

#### S-SSR-002 astro-ssr-detail-with-edge-cache-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: For public, non-personalized CMS-backed Astro detail pages, default to `export const prerender = false` plus `Astro.response.headers.set('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=86400')`. This removes the build-time-only coupling of SSG while allowing an edge cache to serve cached responses. The shared-cache freshness lifetime is 60 seconds; stale responses may be served during revalidation, so this is not a guarantee that every content update appears within 60 seconds. Verify cache behavior on the deployed host. Tags: astro, ssr, edge-cache, architecture, canonical, universal, protected. Status: active. **DEFAULT for public, non-personalized Sanity-backed detail pages.**

#### S-SSR-003 content-batch-prod-rebuild-discipline-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: Every accepted preview-branch content batch MUST conclude with a main-branch merge and Vercel production rebuild. After the site maintainer approves the preview, run `git checkout main && git merge --no-ff preview`, push, wait for the production deployment to succeed, then verify every shipped slug as described in `S-SSR-004`. Adapt branch names to the repository. Every expected public detail route must return 200. Even with SSR detail pages, main must stay current so code, schema, and CSP changes reach production. Tags: deploy-discipline, content-batch, canonical, universal, protected. Status: active. **Mandatory closure for accepted content batches.**

#### S-SSR-004 cms-content-go-live-curl-loop-verification-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: After ANY content-batch production deploy, run a mandatory curl loop on every shipped slug, expecting 200. Source slugs from the published CMS documents' `.slug.current` fields or the accepted Sanity patch payloads. Do not infer slugs from document IDs or workspace names. This illustrative Bash pattern assumes `published_slugs` contains the authoritative slug values:

```bash
verification_failed=0
for slug in "${published_slugs[@]}"; do
  code=$(curl -sS -o /dev/null -w '%{http_code}' \
    "https://resources.example/resources/${slug}/") || code="request-failed"
  printf '%s: %s\n' "$slug" "$code"
  if [ "$code" != "200" ]; then
    verification_failed=1
  fi
done
test "$verification_failed" -eq 0
```

If any request fails or returns a non-200 response, halt release closure. Check the CMS draft/published state, the Vercel deployment state, and whether the route uses SSR or SSG. Fix the root cause, redeploy if needed, and re-verify. A working listing does not prove its destinations work. Tags: deploy, verification, curl-loop, cms, canonical, universal, protected. Status: active.

#### S-SSR-005 astro-sanity-listing-ssr-detail-ssr-with-edge-cache-canonical-recipe-001 [UNIVERSAL]
**Rule**: Default recipe for a public Astro+Sanity resource hub: SSR listing for fresh cards, SSR detail pages with `s-maxage=60, stale-while-revalidate=86400`, and per-slug 200 verification after every production deploy. Use this architecture for new builds unless the site's requirements justify another approach. Combines `S-SSR-001`, `S-SSR-002`, `S-SSR-003`, and `S-SSR-004`. Tags: astro, sanity, ssr, recipe, canonical, universal. Status: active.

#### S-SSR-010 csp-customer-domain-allowlist-not-covered-by-wildcard-001 [PROTECTED, UNIVERSAL]
**Rule**: A CSP wildcard such as `https://*.forms.example` covers that host's subdomains, but NEVER covers a custom hostname such as `https://booking.pottery.example`, even when that hostname CNAMEs to the form vendor. CSP origin matching uses the URL the browser sees, not the DNS-resolved IP. When embedding a vendor form or widget through a custom hostname, explicitly allow that origin in each directive the integration requires. Check `frame-src`, `script-src`, `connect-src`, `form-action`, `img-src`, and `font-src` if fonts are loaded. Do not add it to directives the integration does not use. Tags: csp, custom-domain, allowlist, wildcard, canonical, universal, protected. Status: active.
### AEO content strategy canonicals (UNIVERSAL, reusable)

#### S-SSR-011 sanity-resource-hide-from-listing-flag-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: Add a boolean `hideFromListing` field to the Sanity `resource` document schema. Filter listing, related-resource and collection GROQ queries with `hideFromListing != true`. Do NOT filter the detail-page query (`getResourceBySlug`): the resource stays reachable at its direct URL. Filter targets: `getAllResources`, `getRelatedResources`, top-off/fallback related queries, and product-match + taxonomy-match collection queries. Do NOT filter `getSeriesResources`, because series navigation needs all parts. Audit every query by its purpose rather than assuming one shared filter belongs everywhere. Tags: sanity, resource, hide-from-listing, canonical, universal, protected. Status: active.

#### S-SSR-012 aeo-content-live-but-hidden-from-listing-strategy-canonical-001 [UNIVERSAL]
**Rule**: For articles that should remain publicly accessible and indexable without being promoted in the resource library, hide the listing card via `hideFromListing` (S-SSR-011). The article remains eligible for search indexing and discovery by answer engines, reachable by direct URL, and shareable with customers. Indexing and ranking are not guaranteed. Use cases: a kitchen-equipment maker's comparison guide that is useful on request, an older resource retained for existing customers, or a campaign landing page omitted from general browsing. This is a promotion control, not access control. For content that should not be public, unpublish it or restrict access; for public content that should not appear in search, use `noindex`. Hiding a card does neither. Tags: aeo, seo, content-strategy, hide-from-listing, canonical, universal. Status: active.

### Deploy + diagnosis canonicals (UNIVERSAL)

#### S-SSR-013 astro-script-element-closing-tag-in-docstring-trap-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: NEVER put a literal `</script>` sequence inside a `<script>` element body, including comments, template literals and regular expressions. HTML parsing can treat it as the end of the element regardless of JavaScript comment or string context. Symptom: an Astro production build fails with `Unexpected "*"` or a similar error where a JSDoc block contains an example closing script tag. For example, a form-listener comment might include a complete HTML usage snippet. Fix patterns: (1) move the documentation outside the script into an Astro template comment, (2) use `[script tag]` placeholder notation in documentation, or (3) use `<\/script>` where appropriate inside JavaScript source to avoid the literal closing-tag sequence. Detection: run `rg -n '</script>' -g '*.astro'`; matches should be actual closing tags, not embedded documentation or string content. Tags: astro, esbuild, script-element, docstring, parser-trap, canonical, universal, protected. Status: active.

#### S-SSR-014 deploy-local-astro-build-before-push-discipline-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: Before `git push` on any Astro project, run `npx astro build` locally. The development server and production build use different processing paths, so code that works in `astro dev` can fail in `astro build`. Catching the error locally avoids a failed remote deployment and another feedback cycle. Bake this into automation: a successful local build permits the push; a failed build stops it until the error is surfaced, fixed locally and checked again. A closing script tag embedded in a documentation comment is one example of a defect that a local production build can catch before deployment. Tags: astro, deploy, build, local-test, discipline, canonical, universal, protected. Status: active.

### Reflector dimension added

**Dim 6.5, Post-deploy curl-loop verification gate.** Check that every shipped resource slug returns HTTP 200. This is a HARD Reflector criterion: any 404 requires a CONTINUE verdict. A batch that ships broken resource URLs cannot receive SATISFY. Pair these checks with live production rendering checks: test every slug for reachability, then inspect representative pages for correct rendering.

---

## Curator Log: PublishedOnSite Listing Control

A CMS document can become visible in production listings before its presentation has been reviewed. Make branch-aware listing control a default for new hubs, and apply it consistently across the site's listing queries. This flag controls cards, not access to the underlying pages.

### S-SSR-015 sanity-publishedonsite-flag-with-branch-aware-query-canonical-001 [PROTECTED, UNIVERSAL]
**Rule**: Every resource hub that uses a single CMS dataset for preview and production MUST carry a `publishedOnSite` boolean field on each resource document and an environment-aware filter on every listing query. PROD listings filter with `publishedOnSite == true`. PREVIEW listings ignore that flag. Detail queries (`getResourceBySlug`, `getSeriesResources`) stay UNFILTERED by this flag: direct URLs remain reachable in both environments, even when production cards are hidden. Use CMS drafts or access controls for content that must remain private.

**Branch detection**: on Vercel, read the deployment environment when constructing the query:
```ts
function isProductionBranch(): boolean {
  return (
    typeof process !== 'undefined' &&
    process.env?.VERCEL_ENV === 'production'
  );
}

function publishedFilterClause(): string {
  return isProductionBranch() ? ' && publishedOnSite == true' : '';
}
```

For static pages, this runs at build time; for server-rendered pages, it runs at request time. On other hosts, use the equivalent deployment-environment setting and verify that production is identified correctly.

**Apply to**: every listing GROQ query that returns cards, including `getAllResources`, the `getRelatedResources` pool + fallback, and every collection branch in `getCollectionBySlug`. NEVER apply this listing-control clause to detail or series queries.

**Project `publishedOnSite`** into `RESOURCE_FIELDS` so cards can report their publication status if needed.

**Equivalent pattern**: an existing hub may use an inverted preview flag and an explicit build-time setting to include preview resources. Keep a verified equivalent implementation if migration would introduce risk without adding capability. New builds should use `publishedOnSite` consistently.

### S-SSR-016 publishedonsite-backfill-before-deploy-discipline [PROTECTED, UNIVERSAL]
**Rule**: When adding `publishedOnSite` to an existing hub, backfill `publishedOnSite=true` on every currently published resource BEFORE the new filter reaches production. Otherwise, documents without the field will disappear from listings. Preserve any intentionally staged documents. Pattern for a single atomic transaction through the Sanity mutation API:
```python
ids = client.fetch(
    "*[_type == 'resource' && !(_id in path('drafts.**'))]._id"
)
mutations = [
    {"patch": {"id": resource_id, "set": {"publishedOnSite": True}}}
    for resource_id in ids
]
# POST {"mutations": mutations} to /data/mutate/<dataset>
```

Before submitting, confirm that the selected IDs are exactly the resources intended to remain published. Afterward, verify that every selected document has `publishedOnSite=true` and that the published-resource count is unchanged.

**Order of operations** is critical:
1. Add the `publishedOnSite` filter clause to the query implementation; commit without pushing.
2. Backfill existing published documents with `publishedOnSite=true` through the mutation API.
3. Run `npx astro build` locally to confirm that the code builds.
4. Push the change to a branch and verify that preview still includes staged resources.
5. Merge or deploy to production and verify that the existing cards remain visible.
6. Default new documents to `publishedOnSite=false`; set it to `true` after the site maintainer approves their appearance in production listings.

Reversing this order creates a production window with empty listings. The requests may still succeed, making the broken state easy to miss.

## Curator Log: Spec Sheet Template + PDF Embed

A ceramic studio's resource library needs embedded product spec sheets. Adding this resource format reveals two reusable requirements: PDF embeds need compatible security headers, and product tags need evidence of applicability.

### S-PDF-001 native-pdf-object-csp-gate-canonical [PROTECTED, UNIVERSAL]
**Rule**: A native `<object type="application/pdf" data="https://cdn.sanity.io/...">` embed can render blank when the hub's Content Security Policy blocks the asset host. Before adding the first PDF embed, check BOTH `object-src` and `frame-src`. If Sanity hosts the PDFs, allow `object-src 'self' https://cdn.sanity.io` and include `https://cdn.sanity.io` in `frame-src`. Preserve other required sources. A policy containing `object-src 'none'` blocks the object even when the HTML looks correct. Verify the embed in a browser under the deployed policy and provide a direct PDF link for browsers without an inline viewer. **Why**: source inspection alone cannot reveal a browser-enforced embed failure. **Status**: active.

### S-PDF-003 product-compatibility-tagging [UNIVERSAL]
**Rule**: For a bicycle-parts company's installation guide, tag every product model confirmed to support the described procedure, rather than only the model shown in the example. Guides that require a model-specific feature must remain scoped to models with that feature. Do not infer compatibility from family membership alone; verify it against product documentation. **Why**: readers filter by the product they own, so an applicable guide must appear there without suggesting unsupported compatibility. **Status**: active.

### S-LPACE-001 landing-page-standalone-gets-full-ace-loop [PROTECTED, UNIVERSAL]
**Rule**: A standalone Astro landing page gets the **SAME full ACE loop** as every hub resource. A `design-generator` produces it and a `design-reflector` reviews it against the **9.8/10 HARD** floor, including **AEO structured-snippet readiness** and an **accuracy pass against the source documents**. Add pattern-appropriate JSON-LD, such as WebPage or FAQPage when the visible content supports it, through the site's layout schema mechanism. Do not bypass the review loop because the page lives outside Sanity. For example, a regional bakery chain's catering landing page requires the same review as a customer story in its resource hub. **Why**: an independent reviewer can catch defects the author overlooks. **Status**: active.

## Curator Log: Webinar Build + Review Fixes

### S-WEBINAR-001 webinar-pattern5-video-build-recipe [PROTECTED, UNIVERSAL]
**Rule**: Use the hub's existing video-page pattern for webinar resources when it provides the required layout. Confirm that the detail renderer recognizes the pattern and that the shared stylesheet supplies its styles. Leave `htmlStyles=""` only when shared styles cover the page. Body shape, following an existing working page: an outer page wrapper → a header with the verbatim title and one suitable subtitle → an accessibly labelled video wrapper containing an iframe → a description section with 2–3 prose paragraphs grounded ONLY in the supplied source description. **Embed forms**: YouTube = `https://www.youtube-nocookie.com/embed/<ID>?rel=0` (privacy-enhanced); Vimeo = `https://player.vimeo.com/video/<ID>` (omit `?rel=0`, which is YouTube-specific). iframe attrs: a descriptive `title`, `allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy" referrerpolicy="strict-origin-when-cross-origin"`. **Three build modes** when adding webinars: mode-1 = a webinar with a landing page owned by the business → reuse its approved written content verbatim, plus the embed and an available, verified transcript; mode-2 = a plain YouTube/Vimeo on-demand recording → create the standard source-grounded summary page; mode-3 = a webinar hosted on an external site → create a link-out card only, with no local detail page. Each local page gets its own ACE loop with generator + reflector and the **9.80 HARD** floor. **Why**: a garden-supply shop's recorded demonstrations should use consistent layouts while preserving the distinction between owned content, hosted recordings and external destinations. **Status**: active.

### S-WEBINAR-002 shipped-css-classes-outrank-spec-invented-names [PROTECTED, UNIVERSAL]
**Rule**: When a task specification names an HTML class, verify that the site's actual stylesheet styles it before shipping. Working styles are the implementation reference; a class name in prose can be mistaken. For example, a webinar transcript can render unstyled if its wrapper uses a plausible new name instead of the selector targeted by the existing video-page styles. Check the wrapper, content and speaker selectors together. Flag the discrepancy and correct the specification rather than silently choosing between conflicting instructions. **Verify**: use `rg` to search the site's stylesheets for the proposed selectors, then inspect computed styles in the browser. No matching selector requires investigation; a matching selector still needs the correct ancestor structure and a loaded stylesheet. **Why**: plausible class names do not create styling, and source-text matches alone do not prove that styling reaches the element. **Status**: active.

### S-WEBINAR-003 applyLibraryOrdering-curated-per-filter-ordering [PROTECTED, UNIVERSAL]
**Rule**: To curate resource ORDER within a specific active filter or resource type, use a PRESENTATIONAL stable sort in the library JavaScript. Run `applyLibraryOrdering(filters)` inside `applyFilters` BEFORE pagination. Apply the curated order ONLY while the target filter is active, rank cards using a data attribute such as product family, and restore the saved baseline order when the filter is cleared. Keep card identity keyed by `data-slug` and filtering visibility represented separately from DOM position. Normalize both the ranking keys and card values consistently. Pagination should consume the resulting ordered, visible set; verify that sorting does not change filter membership or lose cards between pages. Example: within a kitchen-equipment maker's maintenance-guide filter, show guides for currently sold products before guides for retired products. Use this option whenever a site needs “show X before Y under filter Z” without changing the order everywhere else. **Why**: local ordering can help readers find relevant material while preserving predictable filtering and pagination. **Status**: active.
### S-WEBINAR-006 parallel-ace-agent-cap-and-recall-discipline [PROTECTED, UNIVERSAL]
**Rule**: Use **4** concurrent local sub-agents as a conservative ceiling, and lower it when available memory requires it. Multiple agents loading separate retrieval models can exhaust memory even while unrelated file writes continue to work. When retrieval is saturated, INLINE the needed context in each agent's task instead of requiring each agent to load its own retrieval stack. Better long-term: retrieve the shared context ONCE in the coordinator and pass the results into agent prompts. Refill available slots as agents complete, keeping concurrency within the limit rather than launching another full wave. **Why**: duplicated retrieval work can make an otherwise manageable resource-library task exceed the machine's memory budget. **Status**: active.
**Additional limits**: The ceiling of 4 applies to agents that do NOT load retrieval models. For agents that load an embedding stack, start with at most **2** at once, avoid running them alongside browser automation, and reduce concurrency further if memory pressure appears. After a crash, run ONE background job at a time until stable operation is verified. Ask every agent to save completed sections incrementally so a crash does not discard all progress. These are starting limits, not guarantees of capacity.

### S-WEBINAR-008 webinar-thumbnails-sanity-hosted-not-hotlinked [PROTECTED, UNIVERSAL]
**Rule**: When a hub's CSP `img-src` allows only `'self'`, `https://cdn.sanity.io`, the site's own domain, and explicitly approved services, hotlinked thumbnails from `img.youtube.com` or `i.vimeocdn.com` are BLOCKED. DOWNLOAD each permitted video thumbnail and UPLOAD it to Sanity (`POST /v2021-06-07/assets/images/production?filename=…`, Content-Type `image/jpeg`, Pillow-resize to approximately 1280 pixels wide). Use the returned Sanity CDN URL as `featuredImage`, a URL STRING when that is what the card renderer expects. Passing a Sanity image OBJECT to a string-only renderer produces `[object Object]`. For YouTube, try `https://img.youtube.com/vi/<ID>/maxresdefault.jpg`, falling back to `hqdefault.jpg`. For Vimeo, obtain the thumbnail URL through oEmbed. Configure type defaults for webinar and video cards so an empty `featuredImage` falls back through `featuredImage || typeDefault || …`. The served card HTML contains the CDN asset hash, not necessarily the upload filename; search for that hash to verify the thumbnail rendered. **Why**: a kitchen-equipment maker's demonstration cards need thumbnails that satisfy the hub's image policy. **Status**: active.

## Curator Log: Standalone comparison landing page

_A standalone HTML landing page was adapted to a resource-hub shell through generation, review, revision, and curation. The reusable lessons concern source fidelity, image handling, structured data, and verification of stored results._

### S-LP-001 landing-page-standalone-preserve-legal-disclaimer [PROTECTED, UNIVERSAL]
**Rule**: When adapting a finished standalone HTML landing page to the hub shell, the shell's generic footer does NOT carry the SOURCE page's own notices. A comparison page's **trademark attributions, comparison date, source references, and qualifications** may live only in its source `<footer>`. Remove the source topbar, logo, and outer document wrappers, but PRESERVE required notice prose **verbatim**, including the source's own date, as a trailing in-body block under the page-specific wrapper. Remove only the footer logo image from that block. Landmark-safe: an in-body `<footer>` inside the shell's `<main>` has an implicit ARIA role of *generic*, rather than creating a second `contentinfo` landmark. The reviewer must assert that every required notice survives before accepting the page. **Why**: stripping decorative page chrome from a bicycle-parts comparison could silently remove attribution and the date that limits the comparison's scope. **Status**: active.

### S-LP-002 lp-image-byte-exact-extract-plus-lcp-attrs [PROTECTED, UNIVERSAL]
**Rule**: (a) Extract a source's inline base64 content images **byte-exactly**: base64-decode them and write the RAW BYTES to the site's public asset directory. NEVER round-trip through Pillow or sharp just to save them; re-encoding changes the bytes and can alter transparency or other approved image properties. Replace every extracted `data:image` reference with its staged asset URL, then verify none remain. Reading the saved file's pixel dimensions with an image library AFTERWARD is fine because inspection does not re-encode it. (b) Give every staged `<img>` explicit intrinsic `width` and `height` from the REAL file dimensions. This reserves layout space, reduces CLS, and addresses missing-dimension audit findings. The above-the-fold LCP hero stays EAGER, with no `loading="lazy"`, and receives `fetchpriority="high"` when it is the priority image. Below-fold images get `loading="lazy" decoding="async"`. **Why**: a garden-supply how-to landing page can preserve its approved artwork while improving loading and layout stability. **Status**: active.

### S-LP-003 no-duplicate-webpage-schema-plus-cta-count [PROTECTED, UNIVERSAL]
**Rule**: Before adding page-level structured data through a layout's `extraSchemas` input, check what the shell ALREADY emits. If the layout attaches `SpeakableSpecification` to a `@type: WebPage` node, adding a separate WebPage node can produce redundant or conflicting page descriptions. Reuse the existing page entity. If the page contains eligible, visible questions and answers and the layout supports a `faq` input, pass them through that input to generate **FAQPage** markup. Add schemas because they describe the content, not to increase a count. Corollary: **CTA count follows the chrome strip**. A “keep every CTA” instruction applies to BODY CTAs; a CTA in the removed topbar leaves WITH that chrome. Reinstating it can introduce a duplicate sticky action. **Why**: a ceramic studio's workshop comparison page should retain its content actions without duplicating the shell's navigation or page schema. **Status**: active.

### S-LP-004 batch-store-tags-not-metadata [tooling]
**Rule**: Check the storage API's item schema before submitting a batch. If it accepts required `content` and `category` fields plus optional top-level `tags`, nesting tags inside an unsupported `metadata` object can reject individual items even when the overall response reports success. For an API that requires comma-separated tags, use `{"content":"Check card destinations","category":"web-craft","tags":"cards,links"}` rather than `{"metadata":{"tags":"cards,links"}}`. Follow the actual schema for other supported fields. ALWAYS verify the per-item results, succeeded and failed counts, and returned identifiers. When practical, retrieve a unique phrase afterward. Never trust an envelope-level `status:ok` alone. **Why**: a successful batch response can conceal failed writes, leaving useful maintenance lessons unavailable later. **Status**: active.

## Curator Log: Product Sheets (link-out cards)

### S-CARD-001 link-out-resource-card-recipe [PROTECTED, UNIVERSAL]
**Rule**: A “link-out” resource, a card in the resource grid that opens a PDF or URL directly with **NO individual on-hub page**, is a **deterministic content operation that needs no ACE loop** when the hub already supports this pattern. Create a `resource` document with: (1) the PDF uploaded as a Sanity **file asset** and referenced through `fileAsset: {_type: "file", asset: {_type: "reference", _ref: "<returned-file-asset-id>"}}`, or use `externalUrl` for an external destination; (2) **NO `htmlBody` or `htmlContent`**, where the route builder explicitly creates detail pages only for documents with a non-empty body; (3) the type supplied through a **taxonomy reference**, where the query derives `resourceType` from the referenced type term rather than reading a stored field; (4) `featuredImage` as a **plain CDN URL string** if required by the renderer. Verify these conventions in the implementation before relying on them. The card CTA opens the destination in a new tab with the type's verb, such as “Download Spec Sheet”. The filter chip appears once the resource-type term exists and the listing query includes it. Create the document and any needed taxonomy changes in ONE atomic Sanity mutation request after uploading the asset. **Why**: a regional bakery chain can publish equipment spec sheets as direct downloads without generating empty detail pages. **Status**: active.

### S-CARD-002 generic-type-thumbnail (CORRECTED: check the existing default first) [PROTECTED, UNIVERSAL]
**Rule**: A card's image resolves through its explicit `featuredImage`, the configured type default, any applicable category fallback, and finally a gradient placeholder. **First read the live type-default configuration**. If the type already has a suitable default, a “generic thumbnail for this type” needs **no work**: leave `featuredImage` empty and let every card inherit it. Only when the type has no default, or the site maintainer wants a different one, generate ONE house-style image. Set it as the type default or explicitly apply it to the documents that need it. Write the house style down once. An invented kitchen-equipment library might use a 4:3 flat-vector composition, terracotta accents, charcoal outlines, a warm cream background, and generous empty space above the subject. Specify no gradients, shadows, or literal text when those are unwanted; naming proposed overlay text can cause an image model to draw it. Generate with an available image tool using securely supplied credentials and a timeout, convert PNG to WebP at quality 90 if appropriate, then upload through Sanity's image-assets API. Read the hub configuration with a direct data query when necessary. A query helper that returns `null` for every projection may be failing itself; that result does not prove the configuration is empty. **Why**: checking inherited defaults prevents unnecessary asset generation and inconsistent card imagery. **Status**: active.

### S-HUB-001 use-case-verbatim-route [PROTECTED, UNIVERSAL]
**Rule**: When a resource type has NO pattern template and the site maintainer supplies a finished, self-contained landing page, preserve that authored page rather than forcing it through a template-extraction process. Preserve `htmlStyles`; clearing page-specific styles is appropriate only when a known shared stylesheet supplies the replacement styling. Wrap the content in a page-specific container, using `<main>` only when the surrounding shell does not already provide it. Keep four touchpoints aligned when introducing the type: its listing label, its CTA text, its display title in every synchronization process, and its Sanity taxonomy term with a Title Case title. Check the LIVE editorial schema before assuming the option is missing, because documentation can become stale. **Why**: a bicycle-parts company's finished customer-story page needs its original styling and consistent type labels throughout the hub. **Status**: active.

### S-HUB-002 scoping-is-bidirectional-hub-collision [PROTECTED, UNIVERSAL] 🔴
**Rule**: Scoping an injected page's CSS protects the HUB from the PAGE and does **nothing** in reverse. An **unscoped** shared rule with a class name reused by the injected page can still affect it. **A scoped rule only competes for properties it DECLARES**; if the source never declares `pointer-events`, increasing specificity on other properties will not help. Add a page-scoped restoration block that reasserts the source's intended values, measured from its standalone rendering. Also add a build-time collision check that stops the build on unguarded conflicts involving layout-critical properties such as `position`, `pointer-events`, `display`, `inset`, `z-index`, and `overflow`. **Why**: a decorative shell rule such as `.feature-grid { position: absolute; inset: 0; pointer-events: none; }` can collide with a garden-supply guide's content grid and make its primary CTA unclickable even when content, structured-data, accessibility, and screenshot checks pass. **Status**: active.

### S-HUB-003 interactive-reachability-gate [PROTECTED, UNIVERSAL]
**Rule**: A test suite that checks only **document properties**, such as text equality, schema validity, and contrast ratios, does not establish **usability**. Add an interactive reachability check for every injected or composed page. For each interactive element, call `scrollIntoView({block: 'center'})`, then assert that `document.elementFromPoint(cx, cy)` returns that element or a descendant at its visible center. Scroll FIRST: an off-viewport element can return `null` and create a false defect. Treat pointer reachability as one check alongside keyboard access and action testing. Ask of every test suite: *“Which check would fail if the page were completely inert?”* If none would fail, the suite is incomplete. **Why**: a ceramic studio's booking link can look correct and pass document checks while an invisible overlay prevents visitors from using it. **Status**: active.
### S-HUB-004 blast-radius-beats-compliance [PROTECTED, UNIVERSAL] 🔴
**Rule**: Never fix a one-page problem by editing a shared hub template, component or stylesheet. Self-contain it in the page, overriding global rules from inside the page's own scope if needed. This holds EVEN WHEN a PROTECTED rule appears to authorise the shared edit. A requirement to clear pre-existing Critical/Serious violations on a route does not remove the need to consider blast radius first. A pre-existing hub-wide defect is a separate decision: report it, never smuggle it into a single-page run. **Why**: a shared edit made for one page puts every other page at risk. For example, a kitchen-equipment guide that needs a `<main>` wrapper may be able to supply it inside its own `htmlBody`, achieving the required DOM structure without changing shared templates. **Status**: active.

### S-HUB-005 look-at-shipped-artefacts-before-the-style-guide [UNIVERSAL]
**Rule**: For any brand-bound visual, OPEN THE SHIPPED FILES before writing a prompt from written design guidance. The guidance is a lossy description; where the two disagree, the shipped work is ground truth. Ground the metaphor in the resource's ACTUAL subject or task, not a generic abstraction: "visually nice" is not "representative". Never negative-prompt away the site's own brand motif. **Why**: a bicycle-parts guide about fitting a luggage rack needs imagery that represents that task. An attractive abstract image may satisfy a template while communicating nothing about the guide. If existing artwork consistently uses recognisable component silhouettes, a prompt that excludes silhouettes contradicts the visual evidence. **Corollary gotcha**: naming overlay text in the composition line ("negative space for the 'Guide' badge") can make Nano Banana 2 RENDER that text; describe the reserved area as an empty gradient. Hub thumbnails carry NO text. **Status**: active.

### S-HUB-006 route-local-override-via-injection-boundary [PROTECTED, UNIVERSAL] 🔴
**Rule**: When shared chrome OUTSIDE your page wrapper carries a defect the route must clear, do NOT edit the shared component. Put an UNSCOPED rule in `htmlStyles`, provided it is injected per resource and delivered on that route alone. Blast radius is a property of the DELIVERY MECHANISM, not the selector: ask "which documents load this CSS?", not "which elements does this selector match?". Use (0,3,0) specificity to beat Astro's scoped `(0,2,0)` deterministically, without `!important`. Verify containment by searching ALL built files for the rule; it must appear in exactly one page document. Also verify that a control route remains unchanged. State the injection-boundary assumption in a comment beside the rule. **This fixes the ROUTE, not the DEFECT**; report the hub-wide item separately. **Why**: a route-local delivery boundary can satisfy a page's accessibility requirements without broadening a one-page task into a shared-component change. **Status**: active.

### S-HUB-007 selectors-from-rendered-dom-not-stylesheet [PROTECTED, UNIVERSAL]
**Rule**: Choose CSS selectors by enumerating `document.querySelectorAll` on the BUILT page, never by searching only the component's stylesheet. A stylesheet lists what COULD exist. **Why**: a garden-supply hub might render `{r.featuredImage ? <img> : <span class="resource-card-fallback">}`. Styling `.resource-card-fallback` changes nothing when every card has an image; the visible label may instead use `.resource-card-label`. Confirm that each intended selector matches the rendered elements before treating the change as complete. Cover both arms of a ternary when the inactive one could return. Rendered markup outranks assumed class names. **Status**: active.

### S-HUB-008 groq-match-is-token-based-not-substring [tooling] 🔴
**Rule**: GROQ `match` TOKENIZES. A query such as `htmlBody match "*preview-bar*"` does not establish that the literal substring exists; token matches elsewhere can produce false positives. For a check that preview-only markup has not leaked into published content, project `htmlBody` and filter in JavaScript for the literal `class="preview-bar"`. Never assert literal containment with `match`; reserve it for token-based search. **Why**: a search result can halt publication even when the target class is absent. The verification must test the exact property the rule requires. **Status**: active.

### S-HUB-009 sanity-only-change-needs-a-real-file-diff [UNIVERSAL]
**Rule**: In a Git-triggered static build without a working content webhook, an edit that lives ONLY in Sanity produces NO Git diff. Vercel may therefore keep serving stale content, with a green previous build and no error. An EMPTY commit is not a reliable trigger. Use a real file diff: maintain a deployment stamp in the repository describing what changed in Sanity and its transaction ID, then commit and push it. **Why**: updating a ceramic studio's related-guide links in Sanity can leave Git reporting "nothing to commit, working tree clean" while the deployed page still contains the old links. **Status**: active.

### S-HUB-010 curl-L-gives-a-false-200-on-an-SSO-gated-preview [tooling]
**Rule**: `curl -sL -o /dev/null -w '%{http_code}'` against an SSO-gated Vercel preview can return **200 for the Vercel LOGIN page** after following the 302. It measures "got a 200", not "got the page". Inspect the UNFOLLOWED response headers with `-D -` and no `-L`, looking for a 302 and a `Location` pointing to Vercel's SSO endpoint. Also inspect the followed body for page-specific content. The same failure underlies token-search false positives and selectors that match no rendered elements: **the instrument answered a different question than the one asked**. **Why**: a successful HTTP response alone does not prove that a preview is publicly reachable. **Status**: active.

### S-HUB-011 link-affordance-hover-AND-focus-visible [UNIVERSAL]
**Rule**: When authored markup wraps a styled `<span>` inside a new `<a>`, the span's own colour and `display:block` can hide the site's generic `a:hover` cue. Add an explicit affordance on BOTH `:hover` and `:focus-visible`; a hover-only cue is invisible to keyboard users. Use `text-decoration:underline; text-underline-offset:3px; text-decoration-thickness:2px` plus a colour shift that maintains AA contrast. Leave the RESTING appearance untouched so the authored look is preserved until interaction. **Why**: a regional bakery chain's related-story link should remain recognisable during both pointer and keyboard interaction without changing the surrounding design. **Status**: active.

### S-REVIEW-001 three-iteration-graduation-exhaustive-iter1 [PROTECTED, UNIVERSAL] 🔴
**Rule**: Target every ACE loop at THREE iterations: generate → ONE EXHAUSTIVE reflection → one fix round → one verification. The first reflection must be **exhaustive, not prioritised**: enumerate EVERYTHING between the artifact and the threshold on every dimension, including one-character items; give the literal fix per item; state explicitly whether each is an **ADD** or a **REPLACE** and quote both sides for a replacement; separate BLOCKERS from ACCEPTED RESIDUALS with reasons so residuals are closed rather than re-litigated; sanity-check each prescription against its surrounding text; declare out-of-scope dependencies, such as unavailable tooling, a shared-file change or a site-owner decision, in the first reflection with evidence. **Why**: a kitchen-equipment video page can accumulate unnecessary rounds when small defects that were visible from the start are discovered one review at a time. Each finding may be correct while the review process remains inefficient. **The mechanism**: a reflection's default audience model optimises for a READER'S ATTENTION by showing the top findings. An ACE loop's scarce resource is ITERATIONS, so limiting the list for readability can work against convergence. **Stop signal for the orchestrator**: a decelerating score curve with shrinking findings means the loop has moved from finding defects to polishing. Demand the complete remaining list in one message, or ship with declared residuals when the required threshold is met. Apply this discipline to reflection as well as final curation, because reflection is where repeated fix rounds originate. **Status**: active.

### S-REVIEW-002 recover-the-reason-before-applying-a-checklist-edit [UNIVERSAL]
**Rule**: Before applying any prescribed edit to positioning-bearing or claim-bearing copy, recover WHY the item exists. Test: *"what would make this edit wrong?"* If you cannot answer, you have not recovered the reason and must not make the edit yet. A checklist compresses a reason into an action; acting on the action alone closes the item and can break the rule it was protecting. **Why**: a reflector instruction to "name the riding context once in the closing sentence" might mean ADD, not REPLACE. Replacing "rear rack" with "commuting" satisfies a superficial wording check while erasing the distinction between the product and its intended use. **Corollary**: long loops encourage this posture. After repeated rounds, the orchestrator may start clearing a queue rather than reasoning about the artifact. This is a CORRECTNESS argument for short loops independent of token cost. **Status**: active.

### S-REVIEW-003: Scoping doctrine has two halves: property AND geometric
**PROTECTED.** Guarding against CSS *property* collisions catches values that lose an override fight,
leaving residue a detector can find. **Geometric collisions leave no residue.**
A ported `scroll-margin-top:24px` may be applied exactly as authored yet fail after the page gains a
72px fixed header it was never designed to accommodate. Whenever `htmlStyles` is preserved, enumerate
every length encoding a distance from a viewport edge and re-measure against the hub's real header.
Verify by measuring the delivered offset of EVERY in-page jump target. A single centre-point hit-test
is scroll-state dependent and can return a confident, meaningless green. In this illustrative layout,
`96px` would allow for the header plus the intended gap; measure the actual result before accepting it.

### S-REVIEW-004: Write the PRINCIPLE, not the mechanism
**PROTECTED.** The geometric-scoping lesson in `S-REVIEW-003` follows from a broader principle:
this markup now renders in a viewport it was not authored for. A rule that names only one mechanism,
such as property overrides, leads subsequent checks to inherit that narrowness, even when the same
author writes them. When writing doctrine, state the principle and let the mechanism stand as one
example, because the next detector will be built from whichever half got written down.

### S-REVIEW-005: A positive control proves failure on ONE input, not coverage
**PROTECTED.** A preview-markup leakage check can miss most pages while its positive control PASSES.
For example, removing extracted style content with `str.replace('', ' ')` shreds a document when a page
emits an empty `<style>` element. If the planted probes happen to land only on unaffected pages, the
control hides the coverage gap. Probe EVERY member of the population, assert
`set(injected) − set(found)` is empty, and report the fraction. Re-derive the control whenever the check
changes, and prove the new control catches the old bug. Add a structural invariant, such as refusing
empty replacement targets, so the silent failure is impossible rather than merely detected.

**UPDATED (a resource-library review): the second way a green control proves nothing.** Coverage
is one failure mode; **provenance of the planted input is the other**. A control can be invalid in a way
its own green result hides: it plants a term the rule never prohibited, so it could not have made the
check fail on any input. Consider an invented garden-supply shop whose editorial policy rejects the
unsupported promise `"never needs watering"`. A control that plants `"easy to maintain"` cannot test
that rule. A corrected control plants the exact prohibited promise and verifies that the check fails.
**So: derive every control from the PRIMARY TEXT, never from the brief, checklist or inherited list
that restates it, and prove the control fires before you trust the check it certifies.**
The generalised root is simple: **a restatement of a rule is not the rule.** Treating a summary as
authoritative can produce an over-blocking word list, a paragraph defending wording against a
nonexistent restriction, or a consequential citation pointing at a file that does not exist. Finding
that a green control was vacuous is worth more than adding another check. Sibling of
`S-HUB-005` (shipped artefacts outrank written design guidance), this applies the same principle
to rules rather than visuals.
### S-REVIEW-006: Enumerate the population; never guess it with an allowlist
**PROTECTED.** An extension allowlist can exclude shipped text files and leave public leaks undetected.
Derive the population from built output, using a null-byte test to identify likely binary files.
Count leaks AFTER every derivation step: per-route markdown alternates generated from built HTML can
multiply one exposed comment across many files. Apply the same rule when finding internal references
in content: enumerate every comment and judge each, rather than grepping only for anticipated markers.
Account for paths and phrases that wrap across line breaks.

### S-REVIEW-007: Orchestrator review is not reflection
**PROTECTED.** Running generator rounds and supplying corrections yourself before involving an independent
reflector reverses the intended generate, reflect, and fix sequence. The orchestrator wrote the
specification and shares its blind spots. Breaking that correlation is the reflector's function.
Use independent reflection before corrective rounds, then verify the fixes. Repeated self-review
does not establish that independently detectable blockers have been removed.

### S-REVIEW-008: `htmlStyles` comments are wire content
**PROTECTED.** `htmlStyles` injects into `<head>`; every `/* comment */` is public. Internal policy labels,
`PROTECTED` markers, process notes and local filesystem paths must not appear there.
For comment-only cleanup, require comment-stripped CSS to remain byte-identical and comment counts
to remain unchanged. This checks that the cleanup preserves executable styles and comment boundaries.
When Sanity is read at build time, a live-page fix needs a redeploy to reach the wire.

---

## Curator Log: Brochure, PDF Resource Page

_Use a fixed evaluation rubric across generation, independent reflection and corrective verification.
Require every dimension to meet the 9.8 graduation threshold before marking the work satisfactory._

_Curate lessons at the end of the loop. Distinguish **VALIDATED** entries, supported by an executed
check, from **PROVISIONAL** entries that remain reasoned proposals. The entries below provide
verification procedures, falsifiers and scope; they do not claim that project-specific execution
evidence ships with this package._

### 🟠 FAQ answers have NO provenance gate (read this before writing FAQ copy)
**A fabricated FAQ answer carrying no numbers can pass a suite that checks only numeric claims.**
For an invented kitchen-equipment maker, try replacing an FAQ answer with: "Every replacement handle
fits every cookware range without an adapter." A numeric checker may leave that unsupported claim
untouched. Adding a fabricated count might trigger the checker, but that would demonstrate sensitivity
to numbers, not to fabrication.

Even if each current answer has been manually verified against a brochure or a named supporting
source, that review does not protect future edits. Add a provenance check binding every FAQ answer
to supporting source text. Calibrate it separately so it accepts faithful paraphrase while rejecting
unsupported claims. Until that check exists and passes its controls, treat FAQ prose as **not covered
by automated provenance checks** and verify each answer by hand. Track the missing check as an open
follow-up rather than presenting a green suite as complete coverage.

### S-GATE-001 gate-assignment-not-just-membership [PROTECTED, UNIVERSAL] 🔴 **PROVISIONAL**
**Rule**: A traceability gate that tests set **MEMBERSHIP** ("every number on the page appears in the
source") is structurally blind to wrong **ASSIGNMENT**. Two values swapped between two nouns are both
still members of the source set. For every attribute-to-entity binding the copy asserts, add a
**second, separate** gate that binds each value to *its own* noun by proximity. Keep membership and
assignment as two gates so each failure message stays diagnostic. **This generalises beyond numbers
to any attribute-to-entity binding**: figure→noun, date→event, catalog number→product, author→guide,
spec→model, finish→product.

**Verification procedure**: Create a fictional bicycle-parts spec sheet listing a compact rack with a
9 kg load limit and a touring rack with a 24 kg load limit. Swap the limits in the rendered copy.
Confirm that the membership check still passes and the assignment check fails. Restore the correct
bindings, confirm both checks pass, and independently inspect every repeated occurrence.

**Falsifier**: A swap mutation on a bound pair that proximity binding fails to reject. Two nouns may
be close enough that both values fall inside both proximity windows. If proximity cannot separate
them, the binding needs a parse rather than a window, and this rule is under-specified for that layout.

**Provenance**: Record the source bindings, failing mutation, corrective implementation and independent
verification with the build's evidence. Promote this entry to validated only after executing the checks.

**Generality**: Claim-bearing pages bind attributes to entities. Membership alone cannot establish
that those bindings are correct. The gap is structural, not specific to a particular artifact.

### S-GATE-002 poison-pill-read-level-sweep-and-two-probe-agreement [PROTECTED, UNIVERSAL] **PROVISIONAL**
**Rule**: When sweeping a gate suite for the "gate grades its own inputs" class, a **verdict-level** sweep
(corrupt a constant, see whether any gate's pass/fail moves) can miss a gate that reads the constant
*inconsequentially*. Build a **read-level** probe instead: replace each content constant with a
**poison-pill object whose every operation raises**: `len`, `in`, iteration, indexing, `str`, `eq`,
`bool` and attribute access. Any gate that touches the constant should raise, whether or not a verdict
would move. **Require agreement between probes of different strength**, while recognising the limits
of both. A single probe's clean result is only a claim about that probe. Each probe needs its own
positive control.

**Verification procedure**: First run a verdict-level sweep across every gate and content constant.
Use a deliberately dependent check as a positive control to prove that the sweep detects verdict
changes. Then run a read-level sweep over the full constant inventory, including route and page-URL
constants. Positive-control the poison pill against operations the gates actually use. Compare the
results, investigating any difference between reading a constant and changing a verdict.

**Falsifier**: A gate that reads a content constant inside a `try/except` that swallows the pill, or via
a C-level path that does not dispatch to its special methods. Either can produce a false clean result.
In that case, add a structural invariant rather than relying only on a stronger pill.

**Provenance**: Retain both sweep results, their constant inventories and their positive-control
outcomes. A verdict-level sweep must not be reported as proof that no constant was read. Promote this
entry to validated only after executing the checks.

**Generality**: Any suite where the checker and the checked content are authored together can contain
this failure mode. Systematic sweeps provide coverage beyond suspected cases, but that coverage
remains bounded by the sweep's definition.

### S-GATE-003 recalibrate-the-instrument-never-reshape-the-artifact [PROTECTED, UNIVERSAL] 🔴 **PROVISIONAL**
**Rule**: When a **prescribed** check fails on an artifact you have independently confirmed is CORRECT,
the finding concerns the **instrument**. Recalibrate the instrument, **declare the deviation from the
prescription in the report**, and keep every control failing where it belongs. Reshaping correct copy
to satisfy a mis-specified gate reverses what is being measured and conceals the problem behind a
passing result. A prescription that permits a calibration pass authorises that recalibration.
Without such permission, report the conflict; do not silently edit correct content to satisfy the check.

**Verification procedure**: For a garden-supply shop's how-to article, test a schema description that
faithfully condenses several body sentences. A rule requiring each description sentence to share
≥ 0.8 token overlap with one body sentence may reject the correct summary because its support is
distributed. Independently verify the source relationship before changing the check. One candidate
calibration is to combine contributing sentences with overlap ≥ 0.25, require their union to cover
≥ 0.8 of the description's content tokens, and check polarity against the best-overlap sentence when
its overlap is ≥ 0.40. Treat these as trial thresholds, not universal semantic guarantees. Confirm
that unsupported summaries and polarity reversals still fail, and have an independent reviewer
reproduce both the original false rejection and the calibrated outcomes.

**Falsifier**: A recalibration that makes a previously caught mutation pass. If any retained control
stops failing, the change weakened the check and this rule was misapplied.

**Provenance**: Record the original prescription, independently verified correct artifact, reason for
the deviation, replacement logic and control results. Promote this entry to validated only after
executing the checks.

**Generality**: A prescribed threshold is a judgement made before testing all real artifacts.
Editing content merely to obtain a passing result can hide a measurement defect.

### S-GATE-004 encode-the-rule-do-not-resolve-to-follow-it [PROTECTED, UNIVERSAL] 🔴 **PROVISIONAL**
**Rule**: A rule written correctly in **prose** and left unencoded is not an automated guard. Turn
enforceable requirements into **build assertions that stop the run**, refusals with non-zero exits,
or equivalent blocking checks. Positive-control each check before trusting it. A soft dependency
that reports UNRESOLVED but stops nothing still allows an artifact to be emitted and handed on.

**Verification procedure**: Exercise both content and reporting guards. (1) For a ceramic studio's
customer story, omit optional `Article.image` data when no image URL exists. If a placeholder such as
`PENDING_IMAGE_URL` survives into the output, require a blocking refusal such as `exit 2`. Test the
placeholder case independently, then confirm that a valid URL and an omitted optional field pass.
(2) For evidence references, check every cited local path with `os.path.exists` and assert the result
during report generation. Deliberately place a referenced file in the wrong directory and confirm
that report generation stops. Correct the reference and verify that the complete report passes.

**Falsifier**: An encoded guard that rejects a correct artifact. The rule may have been encoded at
the wrong level of abstraction and needs the S-GATE-003 treatment, not removal.

**Provenance**: Record the guard, its positive control and the refusal it produced. Promote this entry
to validated only after executing the checks.

**Generality**: Prose rules can be missed during handoff and revision. An executable assertion applies
on every run. A guard that catches its author's mistake demonstrates why the rule needed enforcement.

### S-GATE-005 sanity-file-assets-are-sha1-content-addressed [tooling, UNIVERSAL] **PROVISIONAL**
**Rule**: Sanity **file** assets use content-addressed identifiers incorporating the **SHA-1 of the
source file's bytes**, allowing a candidate CDN URL to be derived before upload:
`https://cdn.sanity.io/files/<projectId>/<dataset>/<sha1>.<ext>`. Validate the URL *shape* against live
siblings first: download them, recompute their SHA-1 hashes and confirm the identifiers match.
Then derive the candidate URL and confirm it exactly against the upload response.

**Consequence**: Page construction and asset ingest can proceed independently once this convention
has been verified. The body can reference the expected final URL before upload, but publication
must wait for the asset to resolve successfully. A 404 may mean "not yet uploaded"; it does not by
itself prove that the derived URL is wrong. An HTTP 404 with `content-type: application/json` is a
response to inspect alongside the upload state, not proof of the cause.

**Caveat**: **Image** asset URLs include dimensions, and delivered formats may depend on content
negotiation. A URL ending in `.webp` can return `content-type: image/jpeg` to a request that does not
advertise WebP support. Inspect `Accept`, response headers and magic bytes before declaring an asset
mismatch.

**Verification procedure**: For a regional bakery chain's downloadable catering guide, compute the
source hash with both `sha1sum` and Python's `hashlib`. Validate the convention against existing file
assets, derive the candidate URL, upload the guide and compare the returned identifier and URL.
Confirm HTTP 200, the expected MIME type and matching downloaded bytes. For an image, repeat requests
with different `Accept` headers and inspect the returned formats.

**Falsifier**: A file asset whose returned hash component differs from the SHA-1 of the uploaded
bytes, for example because an ingest transformation or identifier convention has changed.
Re-derive against a live sibling before relying on the convention for a new extension.

**Provenance**: Retain the local hash, sibling checks, upload response and post-upload retrieval
results. Treat pre-upload derivation as provisional until those checks agree.
### S-GATE-006 articleBody-is-an-assertion-not-a-quotation-channel [UNIVERSAL] **PROVISIONAL**
**Rule**: Treat anything placed in `articleBody` as the page's own published assertion. It is not a separate quotation channel. Moving an unsupported absolute claim out of visible copy and into structured data does **not** soften it. For example, a kitchen-equipment maker should not remove “Fits every kitchen layout” from a product guide while retaining it in the schema. Apply the same evidence and wording checks to structured data as to visible copy.
**Verification**: Inspect both rendered text and structured data for unsupported claims. Prove the check can fail by planting a prohibited example in a test fixture. After changing `articleBody`, update any derived `wordCount` using the same counting method used to generate it.
**Why PROVISIONAL, honestly**: checking consistency between visible copy and structured data is directly testable. The separate claim that answer engines preferentially extract `articleBody` requires retrieval evidence. Without that test, preferential extraction remains a hypothesis, not a demonstrated mechanism.
**Falsifier**: a retrieval test showing answer engines do **not** preferentially source `articleBody` over rendered body text for this page class would weaken that mechanism claim. It would not remove the need for accurate structured data.
**Provenance**: retain the before-and-after content and the check results so another reviewer can reproduce the finding.

### Skill tags applied during review (including corrected assessments)

| Skill | Initial assessment | Follow-up assessment | Final interpretation |
|---|---|---|---|
| Require repeated successful checks before graduation | helpful | helpful | **helpful** |
| Prove that each check can fail | helpful | helpful | **helpful** |
| Sweep related checks for the same fault | *harmful execution* | helpful after correction | **helpful**, see note |
| Distinguish geometric collisions from property conflicts | helpful | not reassessed | **helpful** |
| Compare against relevant shipped work | helpful | helpful | **helpful** |
| Omit unsupported details rather than invent them | *missed* | encoded in checks | **helpful** |
| Require citations to be independently reproducible | *missed* | encoded in checks | **helpful** |
| `sanity-attribute-name-no-at-prefix-001` | helpful | not reassessed | **helpful** |

**Note on the reversal, do not carry the harmful counter.** A sweep can be executed badly even when the underlying rule is sound. Fixing one check that grades its own inputs does not establish that neighboring checks are independent. Adversarial mutations may still pass a suite reported as successful. Repeat the class-wide sweep with probes of different strength, each with its own known-failing control. If those results justify reversing an assessment, retain the reason for the reversal and correct the final tag. The initial criticism concerns the sweep's execution, not necessarily the rule.

### Candidates DROPPED: not supported by the available evidence
Three proposed learnings concerned **image generation**: pass the actual reference artifact rather than describing it in prose; calibrate a “bright core” metric against approved cards; and match a card template by **resource type** before recency. A page-building record that contains no reference inputs, image evaluations, or template comparisons cannot support these findings. If the featured image enters only as an externally produced asset whose Sanity CDN URL is still pending, the page build supplies no evidence about how it was generated.

**These may be useful lessons, but they must come from evidence of the image work itself.** Inspect the prompts, reference inputs, outputs, and evaluations from that work before recording them. A finding that cannot be reproduced from its supporting artifacts does not enter the maintained knowledge base.

### S-GATE-007: Pass the ground-truth artifact as a reference input; do not describe it
**VALIDATED THROUGH ARTIFACT COMPARISON.** `[imagery]` When a subject has a canonical visual reference, supply the file to the generator rather than paraphrasing it into a prompt. Prose alone may not preserve structure.
**Evidence to retain**: the reference, prompts, generated candidates, and comparison results. For a bicycle-parts company's guide illustration, compare attachment points, silhouette, and component proportions against the supplied product image. Keep enough evidence to distinguish a structural correction from an incidental style improvement.
**Procedure**: use the chosen tool's supported reference-image input. Confirm that the file was actually included, then inspect the result against it. A reference can also improve style alignment, but that benefit must be checked separately.
**Falsifier**: a run where the reference is supplied and the structural error persists; or a subject whose ground truth is textual, where a visual reference adds nothing.
**Cross-ref**: apply this principle to every asset class with a visual source of truth. Encode the requirement in the generator's inputs rather than relying on a reminder to follow it.

### S-GATE-008: Match a reference by RESOURCE TYPE before recency
**VALIDATED THROUGH ARTIFACT COMPARISON.** `[imagery]` When calibrating against shipped work, select the most recent artifact **of the same type**, rather than automatically selecting the newest artifact overall.
**Evidence pattern**: a garden-supply shop's newest how-to article and video cards may use flat illustrations, while its product spec-sheet cards use dimensional product renders. Using the newest cards to guide a spec-sheet image can produce a result that belongs to the wrong visual family.
**Falsifier**: a library where resource type does not predict style, making recency a better signal.
**Cross-ref**: this narrows which shipped artifact should guide the work. Remembering “look at shipped work first” is insufficient if the wrong reference is selected.

### S-GATE-009: Calibrate an aesthetic metric against already-approved work before trusting it
**VALIDATED THROUGH CALIBRATION.** `[imagery]` A scoring metric that has never run against known-good input is unvalidated. Start with work already approved for the same visual family.
**Evidence pattern**: a ceramic studio wants to avoid a bright radial halo behind its pieces. A centre-versus-edge luminance test flags new candidates, but also rates approved cards as worse. The test may be detecting the approved diagonal lighting gradient rather than the unwanted radial halo. Test radial falloff directly and compare approved examples with deliberately constructed unwanted examples. Accept the metric only if it distinguishes them.
**Falsifier**: an approved collection so heterogeneous that no single metric can score it consistently, making collection-wide calibration uninformative.
**Cross-ref**: a known-failing control proves detection only for the input chosen. Recalibrate a faulty metric before reshaping acceptable work to satisfy it. Aesthetic judgments still need evidence when automated.

## Curator Log: Guide PDF swap + tagging + titles

_Deterministic content operation, with no authored copy and no ACE loop: replace vetted PDFs on existing guide cards, correct tags, align card titles with document titles, and synchronize the editorial record._

### S-GUIDE-001 swap-a-linked-pdf-on-an-existing-card [PROTECTED, UNIVERSAL]
**Rule**: “New version of the guide, brochure, or spec sheet” means match first, write second.

1. **Match by identity, not by title.** A stable document identifier often survives in the old filename. For a regional bakery chain, an invented identifier such as `BAKE-GUIDE-R7` could distinguish a display guide from a similarly titled ordering guide. Confirm unnumbered pairs using extracted text and manual review. Similarity alone is weak evidence because a substantial revision can change both wording and length.
2. Upload the new PDF **byte-untouched** as a Sanity file asset **with a descriptive filename**. Check that the CDN serves it inline with a readable download filename. This avoids needing a vanity path or a PDF-metadata edit. Verify unchanged bytes by checking that the asset `_id` matches `file-<sha1 of source bytes>-pdf`.
3. Patch **only** `fileAsset` and set `externalUrl` to the same new URL so neither field points to the retired file. Assert in the read-back that every other field is unchanged.
4. Snapshot every document before patching for rollback. Update a representative card first, verify it, then process the rest. Finish with a **population check**: every intended card points to its new asset, and none retains a retired URL. If the operation also changes hosts, verify the host transition across the full population.

**Why**: replacing a file should preserve card identity, metadata, and routing while eliminating stale links. **Status**: active.

### S-GUIDE-002 find-a-type-by-its-live-taxonomy-term-not-its-name [PROTECTED, UNIVERSAL]
**Rule**: Before sweeping “all the X resources,” list live resource-type taxonomy terms **with their reference counts** and select the terms actually in use.

For an invented kitchen-equipment library, a term with slug `setup-guides` might have no references while `equipment-startup` holds the cards displayed as “Setup guide.” A separate `customer-layout-guides` family may also fall within the requested scope. Confirm that scope before applying the sweep.

The editorial record's select value may differ from Sanity's taxonomy slug. Identify the translation between the two stores rather than assuming their names match.

**Why**: querying an obvious but unused slug returns an empty set that can be mistaken for “nothing needs updating.” **Status**: active.

### S-GUIDE-005 card-title-is-the-documents-own-title [UNIVERSAL]
**Rule**: When a card links to a document, use the document's own title from its cover. A descriptive filename can help locate the title, but verify it against the rendered cover before trusting it. Covers often contain graphical text absent from the extracted text layer.

WordPress imports can leave filename-style card titles containing obsolete revision suffixes. Retitle the card when replacing the document, but **never change the slug as part of this operation**: it may serve as both the editorial join key and the public URL.

**Why**: readable titles should remain aligned with the current document without breaking links or record associations. **Status**: active.

---

## Curator Log: a site build's self-heal

_Review the build evidence and extract reusable maintenance lessons. Record additions, updates, and retirements with their supporting checks. Lessons demonstrated on one site enter **PROVISIONAL** until tested on another resource hub._

### S-HEAL-001 second-account-sanity-own-credentials-never-a-shared-tool [PROTECTED, UNIVERSAL]
**Rule**: Operate a Sanity project belonging to a different account with its own credentials and account-scoped tooling. Separation that depends on remembering a flag is fragile.

Read keys from a mode-600 credential file using a parser; never source the file as shell code. Run Wrangler through a wrapper that removes unrelated account variables and refuses an account-pin mismatch. Prove the separation by inspecting the effective environment and recording the count of unrelated variables before and after filtering, without exposing their values.

Verify the live account and project through read-only requests before any write. A public-read dataset does not require a read token in the build. Preserve the established content patterns: polymorphic schemas, atomic mutations, and explicit publication-state fields.

Procedure: [separate-account Sanity and external-writer guidance](05_automations/resource-hub-maintenance/runbook_appendix/second_account_sanity_and_external_writer.md). **Status**: PROVISIONAL.
### S-HEAL-003 a-green-must-be-the-gates-own [PROTECTED, UNIVERSAL] 🔴
**Rule**: Three ways a gate reports a green it did not earn, all closed by reading what the gate itself said: (1) a pipe between the gate and its return code (`| tail; echo rc=$?` reports tail's 0), so redirect to a log and echo the command's own return code; (2) a new rule "proven" by a deliberately faulty input whose finding COUNT matched, so run the OLD gate on the same input and compare the finding TEXT; (3) a PASS over zero inputs, so print the measured count beside every PASS and fail when it is below the expected population. **Why**: a successful return code can conceal a serious axe failure, and matching finding counts can describe unrelated problems. A positive control proves detection for one input, not coverage of the expected population. **Status**: PROVISIONAL.

### S-HEAL-004 gate-log-hash-first [UNIVERSAL]
**Rule**: Line 1 of every gate log is the whole-tree hash of the served directory plus the commit. Use one fixed command to calculate the hash, for example, with `SERVED_DIR` set to the build output:
```bash
find "$SERVED_DIR" -type f -print0 | sort -z | xargs -0 -r sha256sum | sha256sum
```
Hand-off order: commit, final build, gates, report; re-run any log whose hash is not the hand-off's; prove the comparison red once with a planted one-byte change. Mtimes and timestamps are not identity, and a snapshot must be the last write, with later writes declared. **Why**: a log edited after its snapshot no longer matches the captured evidence. **Status**: PROVISIONAL.

### S-HEAL-005 words-over-art-p99-and-line-max [UNIVERSAL]
**Rule**: axe does not grade text over a raster background. For any words on a hero, banner, spotlight or card image: render with the text transparent, take each line box, and gate on the p99 luminance in the box AND the brightest pixel under each line (white text at most 0.3 relative luminance), at every named size and state. Never p95, mean or median. **Why**: a planted 3 px white dot can pass p99 and be caught only by the line maximum. Calibrate on a reviewed resource-library banner before using the check for release decisions. **Status**: PROVISIONAL.

### S-HEAL-006 scrim-graded-on-off-and-bounded [UNIVERSAL]
**Rule**: A scrim is a mix toward its colour, not necessarily a darkening; contrast gates reward any scrim that improves contrast, so grade it by on/off text-transparent captures: never lighter under each line, unchanged (≥0.95 per column) beyond the words plus ~48 px. Bound the fill to the text elements, never a full-width container. A deliberately full-width variant must fail the check. When the image itself is corrected, re-audit and remove compensating scrims that are no longer needed: a workaround can outlive its purpose and become a defect. **Status**: PROVISIONAL.

### S-HEAL-007 judge-what-a-visitor-sees [UNIVERSAL]
**Rule**: Full-page screenshots render sticky/fixed layers at one scroll position, so they never veto a sticky design: capture viewports at named scroll positions. First-screen checks run at the VISIBLE viewport (browser UI shown at load), with heights swept 540-720 at 320-430 widths and small phones (320x568, 360x640, 375x667) included. What the environment cannot emulate is reported "not run", never passed. **Status**: PROVISIONAL.

### S-HEAL-008 astro-global-for-script-created-elements [UNIVERSAL, GOTCHA]
**Rule**: Astro scoped styles reach only elements present at build time (the `data-astro-cid-*` attribute is added then); anything created by client script gets none of the component's `<style>` rules. Style script-created elements with `.parent :global(.child)`, and inject native `<button>`s for JS controls (`role="button"` on an `<li>` breaks the list semantics). **Status**: PROVISIONAL.

### S-HEAL-009 browser-storage-governed-by-purpose [PROTECTED, UNIVERSAL]
**Rule**: Review localStorage, sessionStorage and IndexedDB alongside cookies: classify storage by purpose, not by medium. Distinguish a visitor-set UI preference written on the visitor's own action, such as a pause-motion toggle or language choice, from attribution, analytics, experiment assignments and measurement data written on load. Prefer session-scoped storage when persistence is unnecessary. On hubs with tracking, put non-essential storage behind the consent controls. Verify the applicable requirements before release rather than assuming a storage API is exempt. **Status**: PROVISIONAL.

### S-HEAL-010 cold-reader-and-quantifier-free-constraints [UNIVERSAL]
**Rule**: Before shipping newly authored copy, run one fresh cold reader per review round: provide only the rendered visitor text with page chrome, a fixed audience profile, structured fields for the reader's interpretation, and one open unscripted question. Apply this check to authored copy, not source material that must remain verbatim. Constraints written for a writer carry no quantifiers of their own, such as "only", "never", "every" or "always": amendment wording can become the most authoritative text in the task and pass directly into the copy. **Why**: fresh readers can uncover implications reviewers underestimated, and instructions intended to correct copy can accidentally become published claims. **Status**: PROVISIONAL.

### Deltas this pass
| Op | Skill | Note |
|---|---|---|
| ADD | S-HEAL-003 through S-HEAL-010 | Generic rules defined above |
| UPDATE | Review execution | Limit concurrent context-loading jobs; keep them separate from Playwright runs; use one job at a time after a crash |
| RETIRE | Score-prediction guidance | Evaluate observable evidence instead of predicting review scores |
| RETIRE | Superseded consent guidance | Keep historical notes separate from active instructions |
| CHECK | Duplicate skill IDs | Check heading IDs for duplicates before publishing |
| NOT ADDED | media-005, media-006, media-008, tooling-006, ace-010 | Reuse existing skills rather than duplicating their guidance |

---

## Curator Log: generic edition

- Removed or generalised identifying references, private infrastructure, project history and dependencies that do not ship with this workbench.
- Kept generic lessons, with examples generalised and project-specific directives turned into rules with reasons.
- For future updates, add entries as you build your own hubs, covering choices such as rendering mode, deployment hooks and resource types. Record each lesson with its reason and verification method so a later reader can apply it without private context.
